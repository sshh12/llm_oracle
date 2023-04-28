from typing import List, Dict, Optional
import requests
import datetime
import dateparser
import kalshi_python

from llm_oracle.markets.base import Market, MarketEvent
from llm_oracle import text_utils

config = kalshi_python.Configuration()


class KalshiEvent(MarketEvent):
    def __init__(self, resp_json: Dict):
        self.resp_json = resp_json

    def to_text(self, *args, **kwargs) -> str:
        text = ["Kalshi Market"]
        for key in ["title", "category", "subtitle", "can_close_early"]:
            text.append(f"{key}: {self.resp_json[key]}")
        text.append(f"close_date: {text_utils.future_date_to_string(self.get_end_date())}")
        text.append(text_utils.world_state_to_string())
        return "\n".join(text)

    def get_title(self) -> str:
        return self.resp_json["title"]

    def get_end_date(self) -> datetime.datetime:
        return dateparser.parse(self.resp_json["close_time"])

    def get_market_probability(self) -> float:
        return self.resp_json["last_price"] / 100

    def get_universal_id(self) -> str:
        return "kalshi2:" + self.resp_json["ticker"]

    def is_active(self) -> bool:
        return self.resp_json["status"] == "active"

    def get_market_result(self) -> Optional[float]:
        result = self.resp_json.get("result")
        if result is None or result not in {"yes", "no"}:
            return None
        else:
            return 1.0 if result == "yes" else 0.0


class KalshiMarket(Market):
    def __init__(self, email: str, password: str):
        self.session = kalshi_python.ApiInstance(
            email=email,
            password=password,
            configuration=config,
        )

    def search(self, *args, **kwargs) -> List[Dict]:
        return self.session.get_markets(*args, **kwargs).to_dict()["markets"]

    def get_event(self, event_id: str) -> KalshiEvent:
        return KalshiEvent(self.session.get_market(event_id).to_dict()["market"])
