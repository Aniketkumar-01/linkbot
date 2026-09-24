import os

# Categories for LinkedIn suggestions
CATEGORY_SAME_ROLE = "Same Role"
CATEGORY_INDUSTRY_PEER = "Industry Peer"
CATEGORY_RECRUITER = "Recruiter / Talent"
CATEGORY_THOUGHT_LEADER = "Thought Leader"
CATEGORY_ALUMNI = "Alumni"
CATEGORY_ADJACENT = "Adjacent Role"
CATEGORY_UNKNOWN = "Unknown"

# Default Gemini model
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Search query templates for LinkedIn discovery
SEARCH_TEMPLATES = {
    CATEGORY_SAME_ROLE: 'site:linkedin.com/in/ "{title}" "{skill1}" "{skill2}"',
    CATEGORY_INDUSTRY_PEER: 'site:linkedin.com/in/ "{industry}" "Senior" OR "Lead" "{location}"',
    CATEGORY_RECRUITER: 'site:linkedin.com/in/ "Technical Recruiter" OR "Talent Acquisition" "{industry}" hiring',
    CATEGORY_THOUGHT_LEADER: 'site:linkedin.com/in/ "{industry}" "Director" OR "VP" OR "Head of"',
    CATEGORY_ALUMNI: 'site:linkedin.com/in/ "{education}" "{industry}"',
    CATEGORY_ADJACENT: 'site:linkedin.com/in/ "{skill1}" "{skill2}" "{location}"'
}

# Fallback skills database (if LLM is unavailable)
COMMON_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust",
    "Machine Learning", "Deep Learning", "Data Science", "Data Engineering",
    "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI",
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "CI/CD",
    "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL",
    "Project Management", "Agile", "Scrum", "Product Management"
]
