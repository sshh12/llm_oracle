from prisma import Prisma
from prisma.enums import JobState
from prisma.models import PredictionJob, User
import datetime
import logging
import os
import asyncio


from .predict_llm import validate_question, MODEL_COSTS, MODEL_RUN_FUNCTIONS, MODELS_DEMO_SUPPORTED

MAX_DAILY_DEMO_USES = int(os.environ.get("MAX_DAILY_DEMO_USES", "100"))


async def get_demo_key_recent_uses(prisma: Prisma):
    return await prisma.predictionjob.count(
        where={
            "creditCost": 0,
            "createdAt": {"gte": datetime.datetime.now() - datetime.timedelta(days=1)},
            "state": JobState.COMPLETE,
        }
    )


async def run_job(prisma: Prisma, user: User, job: PredictionJob):
    logging.info(f'Running job {job.id} "{job.question}" for user {user.id}')
    await prisma.predictionjob.update(where={"id": job.id}, data={"state": JobState.RUNNING})

    model_name = job.modelName
    if model_name not in MODEL_RUN_FUNCTIONS:
        await prisma.predictionjob.update(
            where={"id": job.id},
            data={
                "state": JobState.ERROR,
                "errorMessage": f"Model {model_name} is not supported.",
            },
        )
        return

    model_cost = MODEL_COSTS[model_name]

    if user.credits >= model_cost:
        is_demo = False
    else:
        is_demo = True

    if (
        is_demo
        and await get_demo_key_recent_uses(prisma) > MAX_DAILY_DEMO_USES
        or model_name not in MODELS_DEMO_SUPPORTED
    ):
        await prisma.predictionjob.update(
            where={"id": job.id},
            data={
                "state": JobState.ERROR,
                "errorMessage": "Sorry OpenAI is expensive! The daily limit of free uses has run out, buy more predictions, wait a day, or try again.",
            },
        )
        return

    try:
        validation_error, error_explantion = validate_question(job.question)
    except Exception as e:
        logging.error(e)
        await prisma.predictionjob.update(
            where={"id": job.id},
            data={
                "state": JobState.ERROR,
                "errorMessage": "Exception " + str(type(e)),
            },
        )
        return
    if validation_error:
        await prisma.predictionjob.update(
            where={"id": job.id},
            data={
                "state": JobState.ERROR,
                "errorMessage": error_explantion,
            },
        )
        return

    logs = []

    def log_callback(text: str):
        logs.append(text)

    try:
        p = MODEL_RUN_FUNCTIONS[model_name](job.modelTemperature / 100, job.question, log_callback)
        for log_text in logs:
            await prisma.predictionjoblog.create(data={"logText": log_text, "jobId": job.id})
        await prisma.predictionjob.update(
            where={"id": job.id},
            data={
                "state": JobState.COMPLETE,
                "resultProbability": p,
                "creditCost": 0 if is_demo else model_cost,
            },
        )
        if not is_demo:
            await prisma.user.update(where={"id": user.id}, data={"credits": user.credits - MODEL_COSTS[model_name]})
    except Exception as e:
        logging.error(e)
        await prisma.predictionjob.update(
            where={"id": job.id},
            data={
                "state": JobState.ERROR,
                "errorMessage": "Exception: " + str(type(e)),
            },
        )


async def main():
    logging.info("Starting worker")
    prisma = Prisma()
    await prisma.connect()

    while True:
        pending_jobs = await prisma.predictionjob.find_many(where={"state": JobState.PENDING}, include={"user": True})
        for job in pending_jobs:
            await run_job(prisma, job.user, job)
        await asyncio.sleep(30)

    await prisma.disconnect()
