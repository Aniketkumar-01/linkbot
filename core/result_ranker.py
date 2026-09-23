import httpx
import json
import re
from google import genai
from google.genai.errors import APIError
from starlette.concurrency import run_in_threadpool
from .models import UserProfile, LinkedInSuggestion, ActionsResponse

async def rank_and_score_results(user_profile: UserProfile, suggestions: list[LinkedInSuggestion], client: httpx.AsyncClient, gemini_api_key: str = "") -> list[LinkedInSuggestion]:
    """Deduplicates and assigns actions to the suggestions using Gemini."""
    if not suggestions:
        return []
        
    # Deduplicate via one-liner dict comprehension
    unique_suggestions = list({s.url: s for s in suggestions}.values())
    
    if user_profile.name:
        unique_suggestions = [s for s in unique_suggestions if user_profile.name.lower() not in s.name.lower()]
    if user_profile.linkedin_url:
        unique_suggestions = [s for s in unique_suggestions if user_profile.linkedin_url.strip('/') not in s.url]

    if not unique_suggestions or not gemini_api_key:
        return unique_suggestions

    # Construct minimal context for Gemini to save tokens
    candidates_context = [{"url": s.url, "title": s.title, "snippet": s.snippet} for s in unique_suggestions]
    
    prompt = f"""
    You are an expert networking assistant.
    Given this user's profile:
    Name: {user_profile.name}
    Headline: {user_profile.headline}
    Skills: {', '.join(user_profile.skills)}
    
    Determine if the user should "Connect" with or "Follow" the following LinkedIn candidates.
    Recruiters, hiring managers, and close peers should generally be "Connect".
    High-level executives, thought leaders, and adjacent roles should be "Follow".
    
    Candidates: {json.dumps(candidates_context)}
    
    Return a JSON object containing an array of assignments mapping each url to an action ("Connect" or "Follow").
    Structure: {{"assignments": [{{"url": "...", "action": "..."}}]}}
    """
    
    try:
        genai_client = genai.Client(api_key=gemini_api_key)
        response = await run_in_threadpool(
            genai_client.models.generate_content,
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            actions_resp = ActionsResponse(**data)
            action_map = {a.url: a.action for a in actions_resp.assignments}
            for s in unique_suggestions:
                s.action = action_map.get(s.url, "Connect")
    except Exception as e:
        print(f"Gemini action assignment failed, defaulting to Connect: {e}")
        # Default all to Connect if API fails
        for s in unique_suggestions:
            s.action = "Connect"
            
    return unique_suggestions
