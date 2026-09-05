from app.claims import extract_claims


answer = """
Satya Nadella is the Chairman and CEO of Microsoft.
He joined Microsoft in 1992 and became CEO in 2014.
"""

claims = extract_claims(answer)

print("\nEXTRACTED CLAIMS:")
print("=" * 60)

for i, claim in enumerate(claims, start=1):
    print(f"{i}. {claim}")