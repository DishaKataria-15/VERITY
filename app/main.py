from app.search import search_web
from app.extractor import extract_text
from app.llm import generate_answer
from app.claims import extract_claims
from app.verification import match_evidence, verify_claim


def run_verity(question: str):
    print(f"\nQuestion: {question}")
    print("\nSearching the web...\n")

    # --------------------------------------------------
    # 1. Search the web
    # --------------------------------------------------

    results = search_web(question, max_results=3)

    sources = []

    for result in results:
        source = {
            "title": result.get("title", "Untitled"),
            "url": result.get("url", ""),
            "snippet": result.get("content", ""),
            "text": ""
        }

        source["text"] = extract_text(source["url"])

        sources.append(source)

    # --------------------------------------------------
    # 2. Prepare evidence for answer generation
    # --------------------------------------------------

    evidence_parts = []

    for i, source in enumerate(sources, start=1):

        text = source["text"]

        if not text:
            text = source["snippet"]

        evidence_parts.append(
            f"""
SOURCE {i}
Title: {source["title"]}
URL: {source["url"]}

Evidence:
{text[:4000]}
"""
        )

    evidence = "\n".join(evidence_parts)

    # --------------------------------------------------
    # 3. Generate answer
    # --------------------------------------------------

    print("Generating answer with Qwen3...\n")

    answer = generate_answer(question, evidence)

    print("=" * 60)
    print("VERITY ANSWER")
    print("=" * 60)
    print(answer)

    # --------------------------------------------------
    # 4. Extract factual claims
    # --------------------------------------------------

    claims = extract_claims(answer)

    print("\n" + "=" * 60)
    print("FACTUAL CLAIMS")
    print("=" * 60)

    for i, claim in enumerate(claims, start=1):
        print(f"{i}. {claim}")

    # --------------------------------------------------
    # 5. Verify each claim
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("CLAIM VERIFICATION")
    print("=" * 60)

    for i, claim in enumerate(claims, start=1):

        print(f"\nCLAIM {i}")
        print(f"Statement: {claim}")

        # Find the most relevant source
        matched = match_evidence(claim, sources)

        source = matched["source"]

        if not source:
            print("Verdict: INSUFFICIENT_EVIDENCE")
            print("Reason: No relevant evidence was found.")
            continue

        print(f"Best evidence: {source['title']}")
        print(f"Match score: {matched['score']}")

        # Use the matched source as evidence
        matched_evidence = source.get("text", "")

        if not matched_evidence:
            matched_evidence = source.get("snippet", "")

        # Ask the LLM to verify the claim
        verification = verify_claim(
            claim,
            matched_evidence
        )

        print(f"Verdict: {verification['verdict']}")
        print(f"Reason: {verification['reason']}")

        if verification.get("evidence_quote"):
            print(
        f"Evidence: "
        f"{verification['evidence_passage']}"
            )

    # --------------------------------------------------
    # 6. Display sources
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("SOURCES USED")
    print("=" * 60)

    for i, source in enumerate(sources, start=1):

        print(f"{i}. {source['title']}")
        print(f"   {source['url']}")


if __name__ == "__main__":

    question = input("Ask VERITY a question: ")

    run_verity(question)