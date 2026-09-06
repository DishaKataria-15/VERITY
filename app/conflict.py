def analyze_verdicts(verifications: list):
    """
    Analyze verification results from multiple sources.

    Each verification should contain a verdict such as:
    SUPPORTED, WEAKLY_SUPPORTED, CONTRADICTED,
    or INSUFFICIENT_EVIDENCE.
    """

    supported = 0
    weakly_supported = 0
    contradicted = 0
    insufficient = 0

    for verification in verifications:

        verdict = verification.get("verdict", "")

        if verdict == "SUPPORTED":
            supported += 1

        elif verdict == "WEAKLY_SUPPORTED":
            weakly_supported += 1

        elif verdict == "CONTRADICTED":
            contradicted += 1

        elif verdict == "INSUFFICIENT_EVIDENCE":
            insufficient += 1

    # --------------------------------------------------
    # Determine whether reliable evidence disagrees.
    # --------------------------------------------------

    conflict = supported > 0 and contradicted > 0

    if conflict:
        overall_verdict = "DISPUTED"

    elif supported > 0:
        overall_verdict = "SUPPORTED"

    elif contradicted > 0:
        overall_verdict = "CONTRADICTED"

    elif weakly_supported > 0:
        overall_verdict = "WEAKLY_SUPPORTED"

    else:
        overall_verdict = "INSUFFICIENT_EVIDENCE"

    return {
        "overall_verdict": overall_verdict,
        "conflict": conflict,
        "supported": supported,
        "weakly_supported": weakly_supported,
        "contradicted": contradicted,
        "insufficient": insufficient
    }