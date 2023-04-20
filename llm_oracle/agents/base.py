from typing import List, Dict
from abc import ABC, abstractmethod

from llm_oracle.markets.base import MarketEvent


class OracleAgent(ABC):
    @abstractmethod
    def predict_event_probability(self, event: MarketEvent) -> float:
        return
