import re


OUTPUT_PROMPT_P10 = """
Finally, output a score between 0 and 10 (0 = high confident no or P(event) = 0%, 5 = unsure, 10 = high confident yes or P(event) = 100%).

You must use the format "score=...", e.g. score=3 or score=7. Use whole numbers. If you have a probability p [0.0, 1.0], then score = int(p*10).
"""

OUTPUT_PROMPT_P10_SCORE_REGEXES = [r"[Ss]core\s*=\s*(\d+)", r"[Ss]core\s*of\s*(\d+)"]


def parse_p10_output(output: str) -> float:
    for regex in OUTPUT_PROMPT_P10_SCORE_REGEXES:
        score_match = re.search(regex, output)
        if score_match:
            return int(score_match.group(1)) / 10
    raise ValueError(output)


OUTPUT_PROMPT_LIKELY = """
Finally, output a prediction from VERY_UNLIKELY to VERY_LIKELY.

Here are the probabilities of each token:
- VERY_UNLIKELY: 0% - 10%
- UNLIKELY: 10% - 30%
- SOMEWHAT_UNLIKELY: 30% - 45%
- EVEN: 45% - 55%
- SOMEWHAT_LIKELY: 55% - 70%
- LIKELY: 70% - 90%
- VERY_UNLIKELY: 90% - 100%

You must respond with exactly one of the tokens above like `prediction=SOMEWHAT_UNLIKELY` or `prediction=SOMEWHAT_LIKELY`.
"""

LIKELY_MAPPINGS = {
    "VERY_UNLIKELY": 0.05,
    "VERY_LIKELY": 0.95,
    "SOMEWHAT_UNLIKELY": 0.37,
    "SOMEWHAT_LIKELY": 0.62,
    "UNLIKELY": 0.2,
    "LIKELY": 0.8,
    "EVEN": 0.5,
}


def parse_likely_output(output: str) -> float:
    for k, p in LIKELY_MAPPINGS.items():
        if k in output:
            return p
    for k, p in LIKELY_MAPPINGS.items():
        if k.lower().replace("_", "") in output.lower().replace(" ", ""):
            return p
    raise ValueError(output)
