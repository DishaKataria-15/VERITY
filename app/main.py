from app.search import search_web
from app.extractor import extract_text


def run_verity(question: str):
    print(f"\nQuestion: {question}\n")
    print("Searching the web...\n")

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

    return sources


if __name__ == "__main__":
    question = input("Ask VERITY a question: ")

    sources = run_verity(question)

    print("\n" + "=" * 60)
    print("RETRIEVED EVIDENCE")
    print("=" * 60)

    for i, source in enumerate(sources, start=1):
        print(f"\nSOURCE {i}")
        print(f"Title: {source['title']}")
        print(f"URL: {source['url']}")

        if source["text"]:
            print(f"Evidence: {source['text'][:500]}")
        else:
            print("Evidence: Could not extract page content.")