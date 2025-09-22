def validate(text: str, citations: list[str]):
    missing = []
    for claim in text.split("."):
        if claim.strip() and not any(c in claim for c in citations):
            missing.append(claim.strip())
    return {"valid": len(missing) == 0, "missing_citations": missing}
