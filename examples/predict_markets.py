from llm_oracle.markets.kalshi import KalshiMarket
from llm_oracle.markets.custom import CustomMarket, CustomEvent
from llm_oracle.markets.manifold import ManifoldMarket
from llm_oracle.agents.agent_basic import BasicAgentv1, BasicAgentv2, BasicAgentv3
from llm_oracle.agents.agent_tools import ToolAgentv1, ToolAgentv2, ToolAgentv3
import datetime
import os

manifold_market = ManifoldMarket()
kalshi_market = KalshiMarket(email=os.environ["KALSHI_EMAIL"], password=os.environ["KALSHI_PASSWORD"])

kalshi_event_ids = [
    "GTEMP-23-P1.02",
    "NPPC-24DEC31",
    "BIDENVNEBRASKA-24DEC31",
    "TIKTOKBAN-23DEC31",
    "SFFA-COMPLETE",
    "COIN-23DEC31",
    "HURCTOTMAJ-23DEC01-T3",
    "SCOTUSN-23",
    "MOON-25",
]

manifold_event_ids = [
    "will-lex-fridman-interview-ai-by-20",
    "will-biden-be-the-2024-democratic-n",
    "will-a-nuclear-weapon-be-detonated-b71e74f6a8e4",
]

custom_market = CustomMarket(
    [
        CustomEvent(
            "Will a humanity be replaced by AI by 2050?",
            datetime.datetime(2050, 1, 1),
        ),
        CustomEvent(
            "Will a random number that I pull from a uniform distribution [0, 100] be greater or equal to 99?",
            datetime.datetime(2025, 1, 1),
        ),
    ]
)


EVENTS = (
    [kalshi_market.get_event(kid) for kid in kalshi_event_ids]
    + [manifold_market.get_event(mid) for mid in manifold_event_ids]
    + custom_market.events
)

AGENTS = {
    "basic_v1": BasicAgentv1(),
    "basic_v2": BasicAgentv2(),
    "basic_v3": BasicAgentv3(),
    "tool_v1": ToolAgentv1(),
    "tool_v2": ToolAgentv2(),
    "tool_v3": ToolAgentv3(),
}


for event in EVENTS:
    if not event.is_active():
        continue
    title = event.get_title()
    event_uid = event.get_universal_id()
    market_p = event.get_market_probability()
    for agent_name, agent in AGENTS.items():
        p = agent.predict_event_probability(event)
        with open("predictions.tsv", "a") as f:
            f.write(f"{event_uid}\t{title}\t{market_p}\t{agent_name}\t{p}\n")
