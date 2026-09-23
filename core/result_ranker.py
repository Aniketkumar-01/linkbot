import httpx
from .models import UserProfile, LinkedInSuggestion
from utils.constants import CATEGORY_THOUGHT_LEADER, CATEGORY_ADJACENT

def deduplicate_suggestions(suggestions: list[LinkedInSuggestion]) -> list[LinkedInSuggestion]:
    """Removes duplicate suggestions based on LinkedIn URL."""
    seen_urls = set()
    unique = []
    for s in suggestions:
        if s.url not in seen_urls:
            seen_urls.add(s.url)
            unique.append(s)
    return unique

def assign_action(category: str) -> str:
    if category in [CATEGORY_THOUGHT_LEADER, CATEGORY_ADJACENT]:
        return "Follow"
    return "Connect"

async def rank_and_score_results(user_profile: UserProfile, suggestions: list[LinkedInSuggestion], client: httpx.AsyncClient, gemini_api_key: str = "") -> list[LinkedInSuggestion]:
    """Deduplicates and assigns actions to the suggestions."""
    unique_suggestions = deduplicate_suggestions(suggestions)
    
    if user_profile.name:
        unique_suggestions = [s for s in unique_suggestions if user_profile.name.lower() not in s.name.lower()]
    if user_profile.linkedin_url:
        unique_suggestions = [s for s in unique_suggestions if user_profile.linkedin_url.strip('/') not in s.url]
        
    for s in unique_suggestions:
        s.action = assign_action(s.category)
        
    return unique_suggestions
