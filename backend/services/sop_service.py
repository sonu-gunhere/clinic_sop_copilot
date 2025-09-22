import os
import re

SOP_DIR = f"{os.getcwd()}/backend/sops"


def search(query: str):
    results = []
    for file in os.listdir(SOP_DIR):
        if file.endswith(".md"):
            path = os.path.join(SOP_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append({"file": file, "excerpt": content[:200]})
    return {"query": query, "matches": results}


def read(section_id: str):
    file_path = os.path.join(SOP_DIR, section_id + ".md")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return {"section_id": section_id, "content": f.read()}
    return {"error": "Section not found"}
