from app.search import search_web


results = search_web("Who is the current CEO of Microsoft?", max_results=3)

for result in results:
    print("\nTITLE:", result["title"])
    print("URL:", result["url"])
    print("CONTENT:", result["content"][:500])