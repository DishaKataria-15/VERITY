import json
import re

from app.llm import generate_answer


def normalize_text(text: str):
    """
    Normalize whitespace and lowercase text.
    """
    return " ".join(text.lower().split())


def tokenize(text: str):
    """
    Convert text into lowercase words.
    """
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))


def match_evidence(claim: str, sources: list):
    """
    Find the source whose text has the most word overlap with the claim.
    """

    claim_words = tokenize(claim)

    best_source = None
    best_score = 0

    for source in sources:
        text = source.get("text", "")

        if not text:
            text = source.get("snippet", "")

        source_words = tokenize(text)

        if not source_words:
            continue

        overlap = claim_words.intersection(source_words)
        score = len(overlap)

        if score > best_score:
            best_score = score
            best_source = source

    return {
        "claim": claim,
        "source": best_source,
        "score": best_score
    }


def get_candidate_passages(claim: str, evidence: str, max_passages: int = 3):
    """
    Find the most relevant sentences from the evidence.
    """

    sentences = re.split(r"(?<=[.!?])\s+", evidence)

    claim_words = tokenize(claim)

    candidates = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_words = tokenize(sentence)

        if not sentence_words:
            continue

        overlap = claim_words.intersection(sentence_words)
        score = len(overlap)

        if score > 0:
            candidates.append((score, sentence))

    candidates.sort(reverse=True, key=lambda item: item[0])

    return [
        sentence
        for score, sentence in candidates[:max_passages]
    ]


def has_direct_terms(claim: str, evidence: str):
    """
    Check whether important terms from the claim
    are directly present in the evidence.
    """

    stop_words = {
        "the", "a", "an", "is", "are", "was", "were",
        "has", "have", "had", "been", "being",
        "of", "to", "in", "on", "for", "and",
        "or", "that", "this", "he", "she", "it",
        "they", "his", "her", "their", "with",
        "as", "by", "from", "since"
    }

    claim_words = tokenize(claim)
    evidence_words = tokenize(evidence)

    important_words = {
        word
        for word in claim_words
        if word not in stop_words and len(word) > 2
    }

    if not important_words:
        return True

    matched_words = important_words.intersection(evidence_words)

    coverage = len(matched_words) / len(important_words)

    return coverage >= 0.6


def verify_claim(claim: str, evidence: str):
    """
    Verify a claim using a small set of relevant evidence passages.
    """

    passages = get_candidate_passages(claim, evidence)

    if not passages:
        return {
            "verdict": "INSUFFICIENT_EVIDENCE",
            "reason": "No relevant evidence passage was found.",
            "evidence_id": None,
            "evidence_passage": ""
        }

    evidence_block = ""

    for i, passage in enumerate(passages, start=1):
        evidence_block += f"\nEVIDENCE {i}:\n{passage}\n"

    prompt = f"""
You are VERITY's strict claim verification component.

Evaluate the claim using ONLY the numbered evidence passages.

Do not use outside knowledge.
Do not make assumptions.
Do not infer facts that are not explicitly stated.

SUPPORTED:
The evidence directly establishes the claim.

WEAKLY_SUPPORTED:
The evidence provides partial or indirect support.

CONTRADICTED:
The evidence directly conflicts with the claim.

INSUFFICIENT_EVIDENCE:
The evidence does not establish whether the claim is true or false.

Choose exactly one verdict.

If you choose SUPPORTED, WEAKLY_SUPPORTED, or CONTRADICTED,
you MUST select the evidence passage that justifies the verdict.

Return ONLY JSON in this format:

{{
    "verdict": "SUPPORTED",
    "reason": "Short explanation.",
    "evidence_id": 1
}}

Claim:
{claim}

Evidence passages:
{evidence_block}

Do not invent evidence.
Do not create new evidence.
Do not use outside knowledge.
Do not use markdown.
"""

    result = generate_answer(
        question="Verify the claim using the provided evidence.",
        evidence=prompt
    )

    try:
        verification = json.loads(result)

    except json.JSONDecodeError:
        return {
            "verdict": "INSUFFICIENT_EVIDENCE",
            "reason": "The verification result could not be parsed.",
            "evidence_id": None,
            "evidence_passage": ""
        }

    verdict = verification.get("verdict", "")
    evidence_id = verification.get("evidence_id")

    # --------------------------------------------------
    # Validate the evidence ID.
    # --------------------------------------------------

    if verdict in [
        "SUPPORTED",
        "WEAKLY_SUPPORTED",
        "CONTRADICTED"
    ]:

        if not isinstance(evidence_id, int):
            verification["verdict"] = "INSUFFICIENT_EVIDENCE"
            verification["reason"] = (
                "The model did not provide a valid evidence ID."
            )
            verification["evidence_passage"] = ""
            return verification

        if evidence_id < 1 or evidence_id > len(passages):
            verification["verdict"] = "INSUFFICIENT_EVIDENCE"
            verification["reason"] = (
                "The model selected an invalid evidence ID."
            )
            verification["evidence_passage"] = ""
            return verification

    # --------------------------------------------------
    # Get the actual passage ourselves.
    # The LLM does not write the evidence.
    # --------------------------------------------------

    if isinstance(evidence_id, int) and 1 <= evidence_id <= len(passages):

        selected_passage = passages[evidence_id - 1]

        verification["evidence_passage"] = selected_passage

        # --------------------------------------------------
        # Deterministic safeguard:
        # SUPPORTED requires direct textual support.
        # --------------------------------------------------

        if verdict == "SUPPORTED":

            if not has_direct_terms(claim, selected_passage):

                verification["verdict"] = "WEAKLY_SUPPORTED"
                verification["reason"] = (
                    "The selected evidence is related to the claim "
                    "but does not directly establish it."
                )

    else:
        verification["evidence_passage"] = ""

    return verification