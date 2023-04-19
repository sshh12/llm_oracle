from langchain.schema import HumanMessage, SystemMessage
from langchain.input import print_text
from typing import Optional
import re

from llm_oracle import llm
from llm_oracle.agents.abc import OracleAgent
from llm_oracle.markets.abc import MarketEvent


PROMPT_SYSTEM_BASIC_AGENT_V1 = """
You are an expert analyst with tons of already knowledge. You already know everything and you never say "I don't know".

Given the users prediction question, answer to the best of your ability and follow their instructions.
"""

PROMPT_HUMAN_BASIC_AGENT_V1 = """
Predict the outcome of the following event.

{event_text}

Respond with what you already might know about this.

Finally, output a score between 0 and 10 (0 = high confident no or P(event) = 0%, 5 = unsure, 10 = high confident yes or P(event) = 100%).

You must use the format "score=...", e.g. score=3 (for 30%) or score=7 (for 70%)
"""

SCORE_REGEX = r"[Ss]core\s*=\s*(\d+)"


class BasicAgentv1(OracleAgent):
    def __init__(self, verbose: Optional[bool] = True):
        self.llm = llm.get_default_llm()
        self.verbose = verbose

    def predict_event_probability(self, event: MarketEvent) -> float:
        event_text = event.to_text()
        if self.verbose:
            print_text(event_text + "\n", "green")
        human_message = PROMPT_HUMAN_BASIC_AGENT_V1.format(event_text=event_text)
        result = self.llm([SystemMessage(content=PROMPT_SYSTEM_BASIC_AGENT_V1), HumanMessage(content=human_message)])
        if self.verbose:
            print_text(result.content + "\n", "yellow")
        score = re.search(SCORE_REGEX, result.content).group(1)
        return int(score) / 10
