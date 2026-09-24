import asyncio
import logging
import httpx
from utils.constants import (
    SEARCH_TEMPLATES,
    CATEGORY_SAME_ROLE,
    CATEGORY_INDUSTRY_PEER,
    CATEGORY_RECRUITER,
    CATEGORY_THOUGHT_LEADER,
    CATEGORY_ALUMNI,
    CATEGORY_ADJACENT
)
from utils.helpers import clean_linkedin_url, extract_name_from_title, extract_title_from_snippet
from .models import UserProfile, LinkedInSuggestion

logger = logging.getLogger(__name__)

def generate_search_queries(profile: UserProfile) -> dict[str, list[str]]:
    """
    Generates tailored search queries based on the user's profile.
    Returns a dict mapping category to a list of queries.
    """
    queries = {
        CATEGORY_SAME_ROLE: [],
        CATEGORY_INDUSTRY_PEER: [],
        CATEGORY_RECRUITER: [],
        CATEGORY_THOUGHT_LEADER: [],
        CATEGORY_ALUMNI: [],
        CATEGORY_ADJACENT: []
    }
    
    top_skills = profile.skills[:3] if profile.skills else ["Technology"]
    primary_title = profile.job_titles[0] if profile.job_titles else "Software Engineer"
    primary_industry = profile.industries[0] if profile.industries else "Tech"
    loc = profile.location if profile.location else ""
    
    # Same Role
    if len(top_skills) >= 2:
        q = SEARCH_TEMPLATES[CATEGORY_SAME_ROLE].format(title=primary_title, skill1=top_skills[0], skill2=top_skills[1])
        queries[CATEGORY_SAME_ROLE].append(q)
        
    # Industry Peer
    if primary_industry and loc:
        q = SEARCH_TEMPLATES[CATEGORY_INDUSTRY_PEER].format(industry=primary_industry, location=loc)
        queries[CATEGORY_INDUSTRY_PEER].append(q)
        
    # Recruiter
    q = SEARCH_TEMPLATES[CATEGORY_RECRUITER].format(industry=primary_industry)
    queries[CATEGORY_RECRUITER].append(q)
    
    # Thought Leader
    q = SEARCH_TEMPLATES[CATEGORY_THOUGHT_LEADER].format(industry=primary_industry)
    queries[CATEGORY_THOUGHT_LEADER].append(q)
    
    # Alumni
    if profile.education:
        # Just use the first part of the first education entry
        edu_short = str(profile.education[0]).split("-")[0].split(",")[0].strip()
        q = SEARCH_TEMPLATES[CATEGORY_ALUMNI].format(education=edu_short, industry=primary_industry)
        queries[CATEGORY_ALUMNI].append(q)
        
    # Adjacent
    if len(top_skills) >= 2 and loc:
        q = SEARCH_TEMPLATES[CATEGORY_ADJACENT].format(skill1=top_skills[0], skill2=top_skills[1], location=loc)
        queries[CATEGORY_ADJACENT].append(q)
        
    return queries


async def execute_search_serper(query: str, category: str, api_key: str, client: httpx.AsyncClient, max_results: int = 20) -> list[LinkedInSuggestion]:
    """
    Executes a single search using Serper.dev API asynchronously.
    """
    suggestions = []
    try:
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "q": query,
            "num": max_results
        }
        
        response = await client.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        organic_results = data.get("organic", [])
        
        for r in organic_results:
            href = r.get("link", "")
            if "linkedin.com/in/" in href:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                
                name = extract_name_from_title(title)
                job_title = extract_title_from_snippet(snippet)
                clean_url = clean_linkedin_url(href)
                
                suggestions.append(LinkedInSuggestion(
                    name=name,
                    title=job_title,
                    url=clean_url,
                    snippet=snippet,
                    category=category
                ))
    except Exception as e:
        logger.error(f"Serper search error: {e}")
        
    return suggestions

async def search_for_connections(
    profile: UserProfile,
    client: httpx.AsyncClient,
    serper_api_key: str = "",
    progress_callback=None
) -> list[LinkedInSuggestion]:
    """
    Main orchestration function to run searches across multiple categories concurrently.
    """
    if not serper_api_key:
        return []
        
    queries_dict = generate_search_queries(profile)
    
    tasks = []
    for category, queries in queries_dict.items():
        for query in queries:
            tasks.append(execute_search_serper(query, category, serper_api_key, client))
            
    if not tasks:
        return []

    # Execute all searches concurrently for optimal performance
    search_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_suggestions = []
    for res in search_results:
        if isinstance(res, list):
            all_suggestions.extend(res)
        elif isinstance(res, Exception):
            logger.error(f"Concurrent search execution error: {res}")
            
    return all_suggestions
