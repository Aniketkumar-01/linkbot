import json
import httpx
import asyncio
from google import genai
from starlette.concurrency import run_in_threadpool
from .models import UserProfile, LinkedInSuggestion
from utils.constants import CATEGORY_THOUGHT_LEADER, CATEGORY_ADJACENT

async def fetch_jina_content(url: str, client: httpx.AsyncClient, max_length: int = 1500) -> str:
    """
    Fetches the public profile content using Jina Reader asynchronously.
    """
    try:
        jina_url = f"https://r.jina.ai/{url}"
        response = await client.get(jina_url, timeout=10)
        if response.status_code == 200:
            text = response.text
            if len(text) > max_length:
                return text[:max_length] + "..."
            return text
    except Exception:
        pass
    return ""

def deduplicate_suggestions(suggestions: list[LinkedInSuggestion]) -> list[LinkedInSuggestion]:
    """Removes duplicate suggestions based on LinkedIn URL."""
    seen_urls = set()
    unique = []
    for s in suggestions:
        if s.url not in seen_urls:
            seen_urls.add(s.url)
            unique.append(s)
    return unique

def calculate_fast_score(user_profile: UserProfile, suggestion: LinkedInSuggestion) -> float:
    """Calculates a basic relevance score (0.0 to 1.0) using keyword overlap."""
    score = 0.0
    text_to_check = f"{suggestion.title} {suggestion.snippet}".lower()
    
    user_titles = [t.lower() for t in user_profile.job_titles]
    for ut in user_titles:
        if ut in text_to_check:
            score += 0.4
            break
            
    user_skills = [s.lower() for s in user_profile.skills]
    matched_skills = sum(1 for s in user_skills if s in text_to_check)
    if user_skills:
        skill_score = (matched_skills / len(user_skills)) * 0.4
        score += skill_score
        
    if user_profile.industries and user_profile.industries[0].lower() in text_to_check:
        score += 0.1
    if user_profile.location and user_profile.location.lower() in text_to_check:
        score += 0.1
        
    title_lower = suggestion.title.lower()
    if any(keyword in title_lower for keyword in ['director', 'vp', 'head', 'founder', 'partner', 'chief']):
        score += 0.2
    elif any(keyword in title_lower for keyword in ['manager', 'lead', 'principal']):
        score += 0.1
        
    return min(1.0, score)

def assign_action(category: str) -> str:
    if category in [CATEGORY_THOUGHT_LEADER, CATEGORY_ADJACENT]:
        return "Follow"
    return "Connect"

async def gemini_deep_ranking(user_profile: UserProfile, top_suggestions: list[LinkedInSuggestion], client_http: httpx.AsyncClient, api_key: str):
    """
    Uses Gemini to score and provide reasoning for the top suggestions.
    Mutates the suggestions in place.
    """
    try:
        client = genai.Client(api_key=api_key)
        user_context = f"User Profile: {user_profile.headline}, Skills: {', '.join(user_profile.skills)}, Experience: {user_profile.experience_years} years, Location: {user_profile.location}"
        
        jina_contents = []
        tasks = [fetch_jina_content(s.url, client_http) for s in top_suggestions]
        jina_contents = await asyncio.gather(*tasks)

        candidates = []
        for i, s in enumerate(top_suggestions):
            profile_text = jina_contents[i] if jina_contents[i] else s.snippet
            candidates.append(f"[{i}] {s.name} - {s.title} - URL: {s.url}\nExtracted Content/Snippet: {profile_text}\n")
            
        candidates_text = "\n".join(candidates)
        
        prompt = f"""
        You are an elite Senior Psychographic Researcher and Strategic Communication Analyst.
        {user_context}
        Candidates:
        {candidates_text}
        
        For each candidate, return a JSON object with:
        - "index": the index number from the list
        - "score": 0 to 100 representing relevance
        - "reason": a short 1-sentence reason why they should connect
        - "psychological_profile": 1-2 sentences on how they likely think, lead, and work based on their title and snippet.
        - "outreach_strategy": How the user should approach them (e.g., "Be direct and focus on ROI", "Focus on team culture").
        - "connect_message": A highly personalized connection request (STRICT MAXIMUM 300 CHARACTERS).
        
        Return ONLY a JSON array of objects.
        """
        
        response = await run_in_threadpool(
            client.models.generate_content,
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        import re
        match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if not match:
            raise ValueError("No JSON array found in response")
            
        rankings = json.loads(match.group(0))
        
        for r in rankings:
            idx = r.get("index")
            if idx is not None and 0 <= idx < len(top_suggestions):
                top_suggestions[idx].relevance_score = r.get("score", top_suggestions[idx].relevance_score)
                top_suggestions[idx].reason = r.get("reason", "")
                
                # Length limited by model
                raw_msg = r.get("connect_message", "")
                if len(raw_msg) > 300:
                    raw_msg = raw_msg[:297] + "..."
                top_suggestions[idx].connect_message = raw_msg
                
                top_suggestions[idx].psychological_profile = r.get("psychological_profile", "")
                top_suggestions[idx].outreach_strategy = r.get("outreach_strategy", "")
                
    except Exception as e:
        print(f"Deep ranking failed (using fallback scores): {e}")

async def rank_and_score_results(user_profile: UserProfile, suggestions: list[LinkedInSuggestion], client: httpx.AsyncClient, gemini_api_key: str = "") -> list[LinkedInSuggestion]:
    """Deduplicates, scores, and sorts the suggestions."""
    unique_suggestions = deduplicate_suggestions(suggestions)
    
    if user_profile.name:
        unique_suggestions = [s for s in unique_suggestions if user_profile.name.lower() not in s.name.lower()]
    if user_profile.linkedin_url:
        unique_suggestions = [s for s in unique_suggestions if user_profile.linkedin_url.strip('/') not in s.url]
        
    for s in unique_suggestions:
        s.relevance_score = round(calculate_fast_score(user_profile, s) * 100)
        s.action = assign_action(s.category)
        
    unique_suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
    
    if gemini_api_key and unique_suggestions:
        top_n = unique_suggestions[:25]
        await gemini_deep_ranking(user_profile, top_n, client, gemini_api_key)
            
    unique_suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
    return unique_suggestions
