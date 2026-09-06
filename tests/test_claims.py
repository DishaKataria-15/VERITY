from app.claims import extract_claims


answer = """
Satya Nadella succeeded Steve Ballmer as CEO of Microsoft
in 2014 and became Chairman in 2021.
"""

claims = extract_claims(answer)

print("\nEXTRACTED CLAIMS:")
print("=" * 60)

for i, claim in enumerate(claims, start=1):
    print(f"{i}. {claim}")