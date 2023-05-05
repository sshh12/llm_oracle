from typing import Dict
from flask import Flask, render_template, request, redirect, jsonify
from psycopg2 import connect
from pq import PQ
import os

from .models import db, PredictionJob, JobState

app = Flask(__name__, static_folder="../build/static", template_folder="../build")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace("postgres", "postgresql")
db.init_app(app)


def create_job(question: str, model_temp: int, public: bool, user_id: str, job_args: Dict) -> PredictionJob:
    conn = connect(os.environ["DATABASE_URL"])
    pq = PQ(conn)
    job = PredictionJob(
        user_id=user_id,
        question=question,
        model_temperature=model_temp,
        public=public,
        model_custom_api_key=bool(job_args["api_key"]),
    )
    db.session.add(job)
    db.session.commit()
    queue = pq["prediction_jobs"]
    queue.put({**job.to_queue_dict(), **job_args})
    return job


@app.route("/")
def index():
    return render_template("index.html", title="LLM Oracle", desc="Use LLMs to make forecasts about the future.")


@app.route("/results/<job_id>")
def results(job_id):
    job = db.get_or_404(PredictionJob, job_id)
    return render_template("index.html", title=f"LLM Oracle | {job.question}", desc=f"{job.question}")


@app.route("/predict")
def predict():
    question = request.args["q"]
    model_temp = int(request.args["temp"])
    public = bool(request.args["public"])
    api_key = request.args["apikey"]
    user_id = request.args["userId"]
    job = (
        db.session.query(PredictionJob)
        .filter_by(question=question, model_temperature=model_temp, state=JobState.COMPLETE)
        .first()
    )
    if job is None:
        job = create_job(
            request.args["q"], model_temp=model_temp, public=public, user_id=user_id, job_args={"api_key": api_key}
        )
    return redirect("/results/" + str(job.id))


@app.route("/api/jobs/<job_id>")
def get_job(job_id):
    job = db.get_or_404(PredictionJob, job_id)
    return jsonify(job.to_json())


@app.route("/api/jobs")
def get_jobs():
    jobs = db.session.query(PredictionJob).filter_by(public=True, state=JobState.COMPLETE).all()
    return jsonify([job.to_json() for job in jobs])


@app.route("/api/stats")
def get_stats():
    stats = {
        "jobs_complete": db.session.query(PredictionJob).filter_by(state=JobState.COMPLETE).count(),
        "jobs_complete_custom_key": db.session.query(PredictionJob)
        .filter_by(state=JobState.COMPLETE, model_custom_api_key=True)
        .count(),
        "jobs_complete_custom_temp": db.session.query(PredictionJob)
        .filter_by(state=JobState.COMPLETE)
        .filter(PredictionJob.model_temperature != 50)
        .count(),
        "jobs_complete_public": db.session.query(PredictionJob).filter_by(state=JobState.COMPLETE, public=True).count(),
        "jobs_error": db.session.query(PredictionJob).filter_by(state=JobState.ERROR).count(),
        "users_unique": db.session.query(PredictionJob).distinct(PredictionJob.user_id).count(),
    }
    return jsonify(stats)
