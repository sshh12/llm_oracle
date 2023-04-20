from typing import List, Dict
import datetime

from pymanifold import ManifoldClient, LiteMarket

from llm_oracle.markets.base import Market, MarketEvent
from llm_oracle import text_utils


class ManifoldEvent(MarketEvent):
    def __init__(self, event_market: LiteMarket):
        self.event_market = event_market

    def to_text(self, *args, **kwargs) -> str:
        text = ["Manifold Market"]
        text.append(f"question: {self.event_market.question}")
        text.append(f"close_date: {text_utils.future_date_to_string(self.get_end_date())}")
        text.append(text_utils.world_state_to_string())
        return "\n".join(text)

    def get_title(self) -> str:
        return self.event_market.question

    def get_end_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.event_market.closeTime / 1000)

    def get_market_probability(self) -> float:
        return self.event_market.probability

    def get_universal_id(self) -> str:
        return "manifold:" + self.event_market.id


class ManifoldMarket(Market):
    def __init__(self, **kwargs):
        self.client = ManifoldClient(**kwargs)

    def search(self, *args, **kwargs) -> List[Dict]:
        return []

    def get_event(self, event_id: str) -> ManifoldEvent:
        if "-" in event_id:
            me = self.client.get_market_by_slug(event_id)
        else:
            me = self.client.get_market_by_id(event_id)
        return ManifoldEvent(me)
