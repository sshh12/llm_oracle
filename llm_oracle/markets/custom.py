from typing import List, Dict

from llm_oracle.markets.abc import Market, MarketEvent


class CustomEvent(MarketEvent):
    def __init__(self, question: str):
        self.question = question

    def to_text(self, *args, **kwargs) -> str:
        text = ["Prediction Market", f'Will the following statement resolve to yes: "{self.question}"']
        return "\n".join(text)


class CustomMarket(Market):
    def __init__(self, questions: List[str]):
        self.questions = questions

    def search(self, *args, **kwargs) -> List[Dict]:
        return [{"index": i, "question": q} for i, q in enumerate(self.questions)]

    def get_event(self, event_id: str) -> CustomEvent:
        return CustomEvent(self.questions[int(event_id)])
