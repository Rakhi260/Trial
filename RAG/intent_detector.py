def detect_intent(query: str) -> str:
    q = query.lower()

    if any(w in q for w in ["course", "fees", "duration", "syllabus"]):
        return "courses"

    if any(w in q for w in ["intern", "internship", "training", "placement"]):
        return "internship"

    if any(w in q for w in ["about", "sunbeam", "institute"]):
        return "about"

    return "general"
