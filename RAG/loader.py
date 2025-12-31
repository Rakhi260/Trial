import json
import os

def load_sunbeam_data():
    
    # Get absolute path of this file (loader.py)
    base_dir = os.path.dirname(__file__)

    # Go up one level (from RAG → project root), then to scraping/data
    json_path = os.path.join(
        base_dir,
        "..",
        "scraping",
        "data",
        "sunbeam.json"
    )

    json_path = os.path.abspath(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    # ---------- BRANCHES ----------
    branches = data.get("branches", {})
    for branch_name, branch_data in branches.items():
        documents.append({
            "text": branch_data.get("content", ""),
            "title": branch_name,
            "source": branch_data.get("url", ""),
            "branch": branch_name,
            "type": "branch"
        })

    # ---------- MODULAR COURSES ----------
    courses = data.get("modular_courses", {})
    for course_name, course_data in courses.items():
        documents.append({
            "text": f"{course_data.get('name','')}\n{course_data.get('duration','')}",
            "title": course_name,
            "source": course_data.get("url", ""),
            "type": "course"
        })

    return documents
