from typing import Dict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

db = SQLAlchemy()


class JobState(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    ERROR = "error"
    COMPLETE = "complete"


class PredictionJob(db.Model):
    __tablename__ = "prediction_job"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True))
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    state = db.Column(db.Enum(JobState), default=JobState.PENDING)
    public = db.Column(db.Boolean())
    question = db.Column(db.String(300))
    error_message = db.Column(db.String(300), nullable=True)
    model_temperature = db.Column(db.Integer())
    model_custom_api_key = db.Column(db.Boolean())
    result_probability = db.Column(db.Integer(), nullable=True)
    logs = db.relationship("PredictionJobLog", backref="prediction_job", lazy="dynamic")

    def to_queue_dict(self) -> Dict:
        return {"id": str(self.id), "question": self.question}

    def to_json(self) -> Dict:
        logs = list(self.logs)
        logs.sort(key=lambda l: l.date_created)
        return {
            "id": str(self.id),
            "date_created": self.date_created.isoformat(),
            "public": self.public,
            "question": self.question,
            "error_message": self.error_message,
            "model_temperature": self.model_temperature,
            "result_probability": self.result_probability,
            "state": self.state.value,
            "logs": [log.log_text for log in logs],
        }


class PredictionJobLog(db.Model):
    __tablename__ = "prediction_job_log"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    prediction_job_id = db.Column(UUID(as_uuid=True), db.ForeignKey("prediction_job.id"))
    log_text = db.Column(db.Text())
