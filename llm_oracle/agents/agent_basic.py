from typing import Optional

from langchain.schema import HumanMessage, SystemMessage
from langchain.input import print_text

from llm_oracle import llm
from llm_oracle.agents.base import OracleAgent
from llm_oracle.agents.output import OUTPUT_PROMPT, parse_score
from llm_oracle.markets.base import MarketEvent


PROMPT_SYSTEM_BASIC_AGENT_V1 = """
You are an expert analyst with tons of already knowledge. You already know everything and you never say "I don't know".

Given the users prediction question, answer to the best of your ability and follow their instructions.
"""

PROMPT_HUMAN_BASIC_AGENT_V1 = f"""
Predict the outcome of the following event.

{{event_text}}

Respond with what you already might know about this.

{OUTPUT_PROMPT}
"""

PROMPT_HUMAN_BASIC_AGENT_V2 = f"""
Predict the outcome of the following event.

{{event_text}}

Respond with:
* What you learned might know about this.
* Arguments for the event
* Arguments against the event

{OUTPUT_PROMPT}
"""


class BasicAgentv1(OracleAgent):
    def __init__(self, verbose: Optional[bool] = True):
        self.model = llm.get_default_llm()
        self.verbose = verbose

    def get_system_prompt(self) -> str:
        return PROMPT_SYSTEM_BASIC_AGENT_V1

    def get_human_prompt(self) -> str:
        return PROMPT_HUMAN_BASIC_AGENT_V1

    def predict_event_probability(self, event: MarketEvent) -> float:
        event_text = event.to_text()
        if self.verbose:
            print_text(event_text + "\n", "green")
        human_message = self.get_human_prompt().format(event_text=event_text)
        result = self.model([SystemMessage(content=self.get_system_prompt()), HumanMessage(content=human_message)])
        if self.verbose:
            print_text(result.content + "\n", "yellow")
        return parse_score(result.content)


class BasicAgentv2(BasicAgentv1):
    def get_system_prompt(self) -> str:
        return PROMPT_SYSTEM_BASIC_AGENT_V1

    def get_human_prompt(self) -> str:
        return PROMPT_HUMAN_BASIC_AGENT_V2
