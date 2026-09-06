from app.conflict import analyze_verdicts


verifications = [
    {
        "verdict": "SUPPORTED"
    },
    {
        "verdict": "SUPPORTED"
    },
    {
        "verdict": "CONTRADICTED"
    }
]


result = analyze_verdicts(verifications)


print("\nCONFLICT ANALYSIS")
print("=" * 60)

print("Overall verdict:", result["overall_verdict"])
print("Conflict detected:", result["conflict"])
print("Supported:", result["supported"])
print("Weakly supported:", result["weakly_supported"])
print("Contradicted:", result["contradicted"])
print("Insufficient:", result["insufficient"])