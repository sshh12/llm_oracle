import re


OUTPUT_PROMPT = """
Finally, output a score between 0 and 10 (0 = high confident no or P(event) = 0%, 5 = unsure, 10 = high confident yes or P(event) = 100%).

You must use the format "score=...", e.g. score=3 or score=7. Use whole numbers. If you have a probability p [0.0, 1.1], then score=int(p*10).
"""

SCORE_REGEXES = [r"[Ss]core\s*=\s*(\d+)", r"[Ss]core\s*of\s*(\d+)"]


def parse_score(output: str) -> float:
    for regex in SCORE_REGEXES:
        score_match = re.search(regex, output)
        if score_match:
            return int(score_match.group(1)) / 10
    raise ValueError(output)
