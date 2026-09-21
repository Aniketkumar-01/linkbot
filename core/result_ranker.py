import json
import streamlit as st
from google import genai
from .models import UserProfile, LinkedInSuggestion
from utils.constants import CATEGORY_THOUGHT_LEADER, CATEGORY_ADJACENT

def deduplicate_suggestions(suggestions: list[LinkedInSuggestion]) -> list[LinkedInSuggestion]:
    """
    Removes duplicate suggestions based on LinkedIn URL.
    Keeps the first occurrence (which is usually from a higher-priority query).
    """
    seen_urls = set()
    unique = []
    for s in suggestions:
        if s.url not in seen_urls:
            seen_urls.add(s.url)
            unique.append(s)
    return unique

def calculate_fast_score(user_profile: UserProfile, suggestion: LinkedInSuggestion) -> float:
    """
    Calculates a basic relevance score (0.0 to 1.0) using keyword overlap.
    Used for initial sorting before potentially sending to Gemini.
    """
    score = 0.0
    text_to_check = f"{suggestion.title} {suggestion.snippet}".lower()
    
    # 1. Check title overlap
    user_titles = [t.lower() for t in user_profile.job_titles]
    for ut in user_titles:
        if ut in text_to_check:
            score += 0.4
            break
            
    # 2. Check skills overlap
    user_skills = [s.lower() for s in user_profile.skills]
    matched_skills = sum(1 for s in user_skills if s in text_to_check)
    if user_skills:
        skill_score = (matched_skills / len(user_skills)) * 0.4
        score += skill_score
        
    # 3. Check industry/location
    if user_profile.industries and user_profile.industries[0].lower() in text_to_check:
        score += 0.1
    if user_profile.location and user_profile.location.lower() in text_to_check:
        score += 0.1
        
    # 4. Seniority and Decision Maker Boost
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

def gemini_deep_ranking(user_profile: UserProfile, top_suggestions: list[LinkedInSuggestion], api_key: str):
    """
    Uses Gemini to score and provide reasoning for the top suggestions.
    Mutates the suggestions in place.
    """
    try:
        client = genai.Client(api_key=api_key)
        
        user_context = f"User Profile: {user_profile.headline}, Skills: {', '.join(user_profile.skills)}, Experience: {user_profile.experience_years} years, Location: {user_profile.location}"
        
        candidates = []
        for i, s in enumerate(top_suggestions):
            candidates.append(f"[{i}] {s.name} - {s.title} - {s.snippet}")
            
        candidates_text = "\n".join(candidates)
        
        prompt = f"""
        You are an elite Senior Psychographic Researcher and Strategic Communication Analyst. 
        Your expertise combines organizational psychology, psycholinguistics, and professional networking strategy.
        You analyze professional signals to infer deep insights into a person's psychological profile and communication preferences.
        
        {user_context}
        
        Candidates:
        {candidates_text}
        
        For each candidate, return a JSON object with:
        - "index": the index number from the list
        - "score": 0 to 100 representing relevance
        - "reason": a short 1-sentence reason why they should connect
        - "psychological_profile": 1-2 sentences on how they likely think, lead, and work based on their title and snippet.
        - "outreach_strategy": How the user should approach them (e.g., "Be direct and focus on ROI", "Focus on team culture").
        - "connect_message": A highly personalized 2-3 sentence connection request tailored to their psychographic profile.
        
        Return ONLY a JSON array of objects.
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        raw_json = response.text.strip()
        if raw_json.startswith("```json"):
            raw_json = raw_json[7:]
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]
            
        rankings = json.loads(raw_json)
        
        # Update suggestions
        for r in rankings:
            idx = r.get("index")
            if 0 <= idx < len(top_suggestions):
                top_suggestions[idx].relevance_score = r.get("score", top_suggestions[idx].relevance_score)
                top_suggestions[idx].reason = r.get("reason", "")
                top_suggestions[idx].connect_message = r.get("connect_message", "")
                top_suggestions[idx].psychological_profile = r.get("psychological_profile", "")
                top_suggestions[idx].outreach_strategy = r.get("outreach_strategy", "")
                
    except Exception as e:
        st.toast(f"Deep ranking failed (using fallback scores): {e}")

def rank_and_score_results(user_profile: UserProfile, suggestions: list[LinkedInSuggestion], gemini_api_key: str = "") -> list[LinkedInSuggestion]:
    """
    Deduplicates, scores, and sorts the suggestions.
    """
    # 1. Deduplicate
    unique_suggestions = deduplicate_suggestions(suggestions)
    
    # 2. Filter out user's own profile if possible
    if user_profile.name:
        unique_suggestions = [s for s in unique_suggestions if user_profile.name.lower() not in s.name.lower()]
    if user_profile.linkedin_url:
        unique_suggestions = [s for s in unique_suggestions if user_profile.linkedin_url.strip('/') not in s.url]
        
    # 3. Apply fast scoring and set default actions
    for s in unique_suggestions:
        s.relevance_score = calculate_fast_score(user_profile, s)
        s.action = assign_action(s.category)
        
    # Sort by fast score initially
    unique_suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
    
    # 4. Use Gemini to deeply score the top 25 results
    if gemini_api_key and unique_suggestions:
        top_n = unique_suggestions[:25]
        gemini_deep_ranking(user_profile, top_n, gemini_api_key)
        
        # Multiply fast score by 100 for the rest to match 0-100 scale
        for s in unique_suggestions[25:]:
            s.relevance_score = round(s.relevance_score * 100)
    else:
        # Convert fast score (0.0-1.0) to percentage (0-100) for display
        for s in unique_suggestions:
            s.relevance_score = round(s.relevance_score * 100)
            
    # Re-sort after deep ranking
    unique_suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
        
    return unique_suggestions
