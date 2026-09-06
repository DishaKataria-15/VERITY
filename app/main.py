from app.search import search_web
from app.extractor import extract_text
from app.llm import generate_answer
from app.claims import extract_claims
from app.verification import verify_claim
from app.conflict import analyze_verdicts


def run_verity(question: str):
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
    # 2. Prepare evidence
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

    answer = generate_answer(
        question,
        evidence
    )

    # --------------------------------------------------
    # 4. Extract claims
    # --------------------------------------------------

    claims = extract_claims(answer)

    claim_results = []

    # --------------------------------------------------
    # 5. Verify every claim against every source
    # --------------------------------------------------

    for claim in claims:

        verifications = []

        for source in sources:

            source_evidence = source.get("text", "")

            if not source_evidence:
                source_evidence = source.get("snippet", "")

            if not source_evidence:
                continue

            verification = verify_claim(
                claim,
                source_evidence
            )

            verification["source_title"] = source["title"]
            verification["source_url"] = source["url"]

            verifications.append(verification)

        # Analyze agreement/disagreement
        analysis = analyze_verdicts(verifications)

        claim_results.append({
            "claim": claim,
            "verification": verifications,
            "analysis": analysis
        })

    # --------------------------------------------------
    # 6. Return structured result
    # --------------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "claims": claim_results,
        "sources": [
            {
                "title": source["title"],
                "url": source["url"]
            }
            for source in sources
        ]
    }


if __name__ == "__main__":

    question = input("Ask VERITY a question: ")

    result = run_verity(question)

    print("\nVERITY ANSWER")
    print("=" * 60)
    print(result["answer"])

    print("\nCLAIMS")
    print("=" * 60)

    for claim in result["claims"]:

        print(f"\n{claim['claim']}")

        print(
            f"Overall verdict: "
            f"{claim['analysis']['overall_verdict']}"
        )