import re

SKILL_KEYWORDS = [
    "python", "sql", "excel", "data analysis",
    "django", "machine learning", "ml",
    "statistics", "power bi", "tableau"
]

def extract_skills_from_text(text):
    found = set()
    text = text.lower()
    for skill in SKILL_KEYWORDS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill.title())
    return ", ".join(found)
