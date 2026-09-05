from app.search import search_web
from app.extractor import extract_text
from app.llm import generate_answer


def run_verity(question: str):
    print(f"\nQuestion: {question}")
    print("\nSearching the web...\n")

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

    # Combine the retrieved evidence
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

    print("Generating answer with Qwen3...\n")

    answer = generate_answer(question, evidence)

    print("=" * 60)
    print("VERITY ANSWER")
    print("=" * 60)
    print(answer)

    print("\n" + "=" * 60)
    print("SOURCES USED")
    print("=" * 60)

    for i, source in enumerate(sources, start=1):
        print(f"{i}. {source['title']}")
        print(f"   {source['url']}")


if __name__ == "__main__":
    question = input("Ask VERITY a question: ")

    run_verity(question)