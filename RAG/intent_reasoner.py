def is_general_sunbeam_question(query: str) -> bool:
    triggers = [
        "what do you think",
        "is sunbeam good",
        "should i join",
        "opinion",
        "worth it",
        "recommend",
        "good institute"
    ]

    q = query.lower()
    return any(t in q for t in triggers)
