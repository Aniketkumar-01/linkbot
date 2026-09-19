import re

def extract_linkedin_username(url: str) -> str:
    """Extracts username from a LinkedIn URL."""
    if not url:
        return ""
    match = re.search(r'linkedin\.com/in/([^/?]+)', url)
    return match.group(1) if match else url

def normalize_score(score: int, min_score: int = -20, max_score: int = 100) -> int:
    """Normalizes score to 0-100 scale."""
    if score >= max_score:
        return 100
    if score <= min_score:
        return 0
    return int(((score - min_score) / (max_score - min_score)) * 100)
