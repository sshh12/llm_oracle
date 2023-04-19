from typing import List, Dict
import kalshi

from llm_oracle.markets.abc import Market, MarketEvent


class KalshiEvent(MarketEvent):
    def __init__(self, resp_json: Dict):
        self.resp_json = resp_json

    def to_text(self, *args, **kwargs) -> str:
        text = ["Kalshi Market"]
        for key in ["title", "category", "settle_details", "metrics_tags", "underlying"]:
            text.append(f"{key}: {self.resp_json[key]}")
        text.append(f'settlement_sources: {[s["url"] for s in self.resp_json["settlement_sources"]]}')
        return "\n".join(text)


class KalshiMarket(Market):
    def __init__(self, email: str, password: str):
        self.session = kalshi.Session(email=email, password=password)

    def search(self, *args, **kwargs) -> List[Dict]:
        return []

    def get_event(self, event_id: str) -> KalshiEvent:
        return KalshiEvent(self.session.get_market_cached(event_id)["market"])
