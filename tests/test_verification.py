from app.verification import match_evidence, verify_claim


claim = "Satya Nadella is the CEO of Microsoft."
sources = [
    {
        "title": "Microsoft Leadership",
        "url": "https://example.com/microsoft",
        "text": """
        Satya Nadella is Chairman and Chief Executive Officer
        of Microsoft.
        """
    },
    {
        "title": "Random Article",
        "url": "https://example.com/random",
        "text": """
        Microsoft was founded in 1975 by Bill Gates and Paul Allen.
        """
    }
]


matched = match_evidence(claim, sources)

print("\nCLAIM:")
print(claim)

print("\nBEST MATCH:")
print(matched["source"]["title"])

evidence = matched["source"]["text"]

verification = verify_claim(claim, evidence)

print("\nVERIFICATION:")
print("Verdict:", verification["verdict"])
print("Reason:", verification["reason"])