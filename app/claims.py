import json
from app.llm import generate_answer


def extract_claims(answer: str):
    """
    Extract independently verifiable factual claims from an answer.
    """

    prompt = f"""
You are VERITY's claim extraction component.

Read the answer below and identify ALL factual claims it makes.

A factual claim is a statement that can be independently checked
against evidence.

IMPORTANT RULES:

1. Each claim must contain ONLY ONE independently verifiable fact.

2. If a sentence contains multiple factual statements joined by
"and", "but", "while", or similar words, SPLIT them into separate
claims.

3. Do not combine different facts into one claim.

4. Preserve important details such as:
   - people
   - organizations
   - dates
   - numbers
   - locations
   - events

5. Do not add information that is not present in the answer.

6. Do not include opinions, explanations, or reasoning unless they
contain a factual statement that can be independently verified.

Example:

Answer:
"Satya Nadella became CEO of Microsoft in 2014 and became Chairman
in 2021."

Correct output:

[
    "Satya Nadella became CEO of Microsoft in 2014.",
    "Satya Nadella became Chairman of Microsoft in 2021."
]

Another example:

Answer:
"Microsoft was founded in 1975 by Bill Gates and Paul Allen."

Correct output:

[
    "Microsoft was founded in 1975.",
    "Bill Gates co-founded Microsoft.",
    "Paul Allen co-founded Microsoft."
]

Return ONLY a JSON array of strings.

Do not add explanations.
Do not use markdown.
Do not add information from outside the answer.

Answer:
{answer}
"""

    result = generate_answer(
        question="Extract independently verifiable factual claims.",
        evidence=prompt
    )

    try:
        claims = json.loads(result)

        if isinstance(claims, list):

            # Keep only non-empty strings
            clean_claims = [
                claim.strip()
                for claim in claims
                if isinstance(claim, str) and claim.strip()
            ]

            return clean_claims

    except json.JSONDecodeError:
        pass

    return []