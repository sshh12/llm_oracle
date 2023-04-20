from typing import List, Dict, Optional
import datetime

from llm_oracle.markets.base import Market, MarketEvent
from llm_oracle import text_utils, processing_utils


class CustomEvent(MarketEvent):
    def __init__(self, question: str, close_date: datetime.datetime, prior: Optional[float] = 0.5):
        self.question = question
        self.close_date = close_date
        self.prior = prior

    def to_text(self, *args, **kwargs) -> str:
        text = ["Prediction Market"]
        text.append(f'Will the following statement resolve to yes by the close date: "{self.question}"')
        text.append(f"close_date: {text_utils.future_date_to_string(self.get_end_date())}")
        text.append(text_utils.world_state_to_string())
        return "\n".join(text)

    def get_title(self) -> str:
        return self.question

    def get_end_date(self) -> datetime.datetime:
        return self.close_date

    def get_market_probability(self) -> float:
        return self.prior

    def get_universal_id(self) -> str:
        return "custom:" + processing_utils.hash_str(repr([self.question, self.close_date]))

    def to_dict(self) -> Dict:
        return {"question": self.question, "close_date": self.close_date}


class CustomMarket(Market):
    def __init__(self, events: List[MarketEvent]):
        self.events = events

    def search(self, *args, **kwargs) -> List[Dict]:
        return [event.to_dict() for event in self.events]

    def get_event(self, event_id: str) -> CustomEvent:
        return self.events[int(event_id)]
