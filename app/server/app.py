from typing import Dict
from flask import Flask, render_template, request, redirect, jsonify
from psycopg2 import connect
from pq import PQ
import os

from .models import db, PredictionJob

app = Flask(__name__, static_folder="../build/static", template_folder="../build")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace("postgres", "postgresql")
db.init_app(app)


def create_job(question: str, model_temp: int, job_args: Dict) -> PredictionJob:
    conn = connect(os.environ["DATABASE_URL"])
    pq = PQ(conn)
    job = PredictionJob(question=question, model_temperature=model_temp, model_custom_api_key=bool(job_args["api_key"]))
    db.session.add(job)
    db.session.commit()
    queue = pq["prediction_jobs"]
    queue.put({**job.to_queue_dict(), **job_args})
    return job


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results/<job_id>")
def results(job_id):
    return render_template("index.html")


@app.route("/predict")
def predict():
    job = create_job(
        request.args["q"], model_temp=int(request.args["temp"]), job_args={"api_key": request.args["apikey"]}
    )
    return redirect("/results/" + str(job.id))


@app.route("/api/jobs/<job_id>")
def get_job(job_id):
    job = db.get_or_404(PredictionJob, job_id)
    return jsonify(job.to_json())
