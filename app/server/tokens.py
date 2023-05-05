import datetime
import os

from .models import PredictionJob


MAX_DAILY_DEMO_USES = int(os.environ.get("MAX_DAILY_DEMO_USES", "100"))


def get_demo_key_recent_uses(session) -> int:
    now = datetime.datetime.utcnow()
    yesterday = now - datetime.timedelta(days=1)
    demo_uses = (
        session.query(PredictionJob)
        .filter_by(model_custom_api_key=False)
        .filter(PredictionJob.date_created > yesterday)
        .count()
    )
    return demo_uses
