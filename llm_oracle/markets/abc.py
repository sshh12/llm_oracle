from typing import List, Dict
from abc import ABC, abstractmethod


class MarketEvent(ABC):
    @abstractmethod
    def to_text(self, *args, **kwargs) -> str:
        return


class Market(ABC):
    @abstractmethod
    def search(self, *args, **kwargs) -> List[Dict]:
        return

    @abstractmethod
    def get_event(self, event_id: str) -> MarketEvent:
        return
