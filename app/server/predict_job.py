from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pq import PQ
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import CallbackManager
import logging
import os

from .models import db, PredictionJob, PredictionJobLog, JobState
from .llm_model import validate_question, run_agent, LLMEventLoggingCallback


def run_job(db, api_key: str, job: PredictionJob):
    job.state = JobState.RUNNING
    db.session.commit()

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
        api_key = job_item.data["api_key"] if job.model_custom_api_key else os.environ["OPENAI_API_KEY"]
        run_job(db, api_key=api_key, job=job)
