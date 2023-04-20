from typing import List, Dict
import datetime
import dateparser
import kalshi

from llm_oracle.markets.base import Market, MarketEvent
from llm_oracle import text_utils


class KalshiEvent(MarketEvent):
    def __init__(self, resp_json: Dict):
        self.resp_json = resp_json

    def to_text(self, *args, **kwargs) -> str:
        text = ["Kalshi Market"]
        for key in ["title", "category", "settle_details", "metrics_tags", "underlying"]:
            text.append(f"{key}: {self.resp_json[key]}")
        text.append(f'settlement_sources: {[s["url"] for s in self.resp_json["settlement_sources"]]}')
        text.append(f"close_date: {text_utils.future_date_to_string(self.get_end_date())}")
        text.append(text_utils.world_state_to_string())
        return "\n".join(text)

    def get_title(self) -> str:
        return self.resp_json["title"]

    def get_end_date(self) -> datetime.datetime:
        return dateparser.parse(self.resp_json["close_date"])

    def get_market_probability(self) -> float:
        return self.resp_json["last_price"] / 100


class KalshiMarket(Market):
    def __init__(self, email: str, password: str):
        self.session = kalshi.Session(email=email, password=password)

    def search(self, *args, **kwargs) -> List[Dict]:
        return []

    def get_event(self, event_id: str) -> KalshiEvent:
        return KalshiEvent(self.session.get_market_cached(event_id)["market"])
