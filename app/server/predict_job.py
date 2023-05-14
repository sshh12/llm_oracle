from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pq import PQ
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import CallbackManager
import logging
import os

from .models import db, PredictionJob, PredictionJobLog, JobState, User
from .predict_llm import validate_question, run_agent, LLMEventLoggingCallback
from .tokens import get_demo_key_recent_uses, MAX_DAILY_DEMO_USES


def run_job(db, user: User, api_key: str, job: PredictionJob, use_shared_key: bool):
    job.state = JobState.RUNNING
    db.session.commit()

    if user.predictions_remaining > 0 or not use_shared_key:
        is_demo = False
    else:
        is_demo = True

    if is_demo and get_demo_key_recent_uses(db.session) > MAX_DAILY_DEMO_USES:
        job.state = JobState.ERROR
        job.error_message = "Sorry GPT4 is expensive! The daily limit of free uses has run out, buy more predictions or set your personal OpenAI API in settings and try again."
        db.session.commit()
        return

    class LoggingCallback(LLMEventLoggingCallback):
        def write_log(self, text: str):
            log = PredictionJobLog(log_text=text)
            job.logs.append(log)
            db.session.commit()

    callback_manager = CallbackManager([LoggingCallback()])

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-4",
        request_timeout=120,
        max_retries=10,
        temperature=job.model_temperature / 100,
        callback_manager=callback_manager,
    )
    tool_llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        request_timeout=120,
        max_retries=10,
        temperature=job.model_temperature / 100,
    )

    try:
        validation_error, error_explantion = validate_question(llm, job.question)
    except Exception as e:
        logging.error(e)
        job.state = JobState.ERROR
        job.error_message = "Exception " + str(type(e))
        db.session.commit()
        return
    if validation_error:
        job.state = JobState.ERROR
        job.error_message = error_explantion
        db.session.commit()
        return

    try:
        p = run_agent(llm, tool_llm, job.question, callback_manager)
        job.state = JobState.COMPLETE
        job.result_probability = p
        if use_shared_key and not is_demo:
            user.predictions_remaining -= 1
    except Exception as e:
        logging.error(e)
        job.state = JobState.ERROR
        job.error_message = "Exception: " + str(type(e))

    db.session.commit()


def main():
    logging.info("Starting worker")
    engine = create_engine(os.environ["DATABASE_URL"].replace("postgres", "postgresql"))
    conn = connect(os.environ["DATABASE_URL"])
    db.session = Session(engine)
    pq = PQ(conn)
    queue = pq["prediction_jobs"]
    while True:
        job_item = queue.get(block=True)
        if job_item is None:
            continue
        job = db.get_or_404(PredictionJob, job_item.data["id"])
        logging.info(f"Running for {job_item.data}")
        user_id = job_item.data["user_id"]
        user = db.get_or_404(User, user_id)
        api_key = job_item.data["api_key"] if job.model_custom_api_key else os.environ["OPENAI_API_KEY"]
        run_job(
            db,
            user=user,
            api_key=api_key,
            job=job,
            use_shared_key=not job.model_custom_api_key,
        )
