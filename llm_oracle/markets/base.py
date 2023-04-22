from typing import List, Dict
import datetime
from abc import ABC, abstractmethod


class MarketEvent(ABC):
    @abstractmethod
    def to_text(self, *args, **kwargs) -> str:
        return

    @abstractmethod
    def get_end_date(self) -> datetime.datetime:
        return

    @abstractmethod
    def get_market_probability(self) -> float:
        return

    @abstractmethod
    def get_title(self) -> str:
        return

    @abstractmethod
    def get_universal_id(self) -> str:
        return

    @abstractmethod
    def is_active(self) -> bool:
        return


class Market(ABC):
    @abstractmethod
    def search(self, *args, **kwargs) -> List[Dict]:
        return

    @abstractmethod
    def get_event(self, event_id: str) -> MarketEvent:
        return
