import json
from app.llm import generate_answer


def extract_claims(answer: str):
    """
    Extract factual claims from an answer.
    """

    prompt = f"""
You are a claim extraction component of VERITY.

Read the answer below and identify the factual claims it makes.

A factual claim is a statement that can be checked against evidence.

Return ONLY a JSON array of strings.

Example:
[
    "Satya Nadella is the CEO of Microsoft.",
    "Satya Nadella joined Microsoft in 1992.",
    "Satya Nadella became CEO in 2014."
]

Do not add explanations.
Do not use markdown.

Answer:
{answer}
"""

    result = generate_answer(
        question="Extract the factual claims from this answer.",
        evidence=prompt
    )

    try:
        claims = json.loads(result)

        if isinstance(claims, list):
            return claims

    except json.JSONDecodeError:
        pass

    return []