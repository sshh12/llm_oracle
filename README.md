# llm_oracle

<img width="695" alt="screenshot" src="https://user-images.githubusercontent.com/6625384/235320624-75ab6c5d-8722-45f9-8a3b-d3cd96d03063.png">

LLM Oracle is a GPT-4 powered tool for predicting future events. It's like a [Magic 8 Ball](https://en.wikipedia.org/wiki/Magic_8_Ball) that is able to perform basic research, calculations, and reasoning.

[Demo Site](https://oracle.sshh.io/)

## How Does This Work?

### Prompting

At a high level this entire thing is just a wrapper for [GPT-4](https://openai.com/research/gpt-4).

1. You ask a question
2. We ask GPT `Is {question} a valid question for a prediction market?`, if not ERROR
3. We ask GPT

```
Will the answer to "{question}" be yes?
Today is {date}

You can use these tools: Calculator, Wolfram Alpha, Google, etc.

Respond with arguments for and against, then with a final prediction.
```

4. GPT enters a prompt chain ([ReAct](https://www.promptingguide.ai/techniques/react)) to gather information to best answer the question
5. We parse the final prediction (like `SOMEWHAT_LIKELY`) into a probability between 0 and 100%.

### Limitations

- The outputs of the model are not expected to be calibrated (e.g. of the events it says 80%, is possible only 50% end up being correct)
- The model is limited to what is obviously google-able to answer the question. It can not perform detailed research, build forecasting models, and run advanced multipart calculations.
- The typical limitations of LLMs also apply like vulnerability to prompt injections in both the question and gathered internet text, hallucinations, bias, etc.

## App Privacy

Here's a quick overview of what's saved when you use the demo app. In the event of a breach, this is also what could be obtained.

#### Stored "Forever"

- The questions you ask (anyone with the prediction ID or anyone generally if "public" set in settings can view)
- A unique anonymous user id associated with the questions (you can bypass with new browser, incognito, etc)
- The GPT agent logs which may contain publically obtainable information about the question

#### Not Used / Stored

- Social media accounts you share with

## Python API

### Install

1. `pip install git+https://github.com/sshh12/llm_oracle`
2. Environment

```
OPENAI_API_KEY=
SERPER_API_KEY= (required for tool agents)
SCRAPINGBEE_API_KEY= (required for tool agents)
WOLFRAM_ALPHA_APPID= (required for tool agents)
KALSHI_EMAIL= (required for kalshi API)
KALSHI_PASSWORD= (required for kalshi API)

DATABASE_URL= (required for demo app)
```

### Example

```python
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

```
