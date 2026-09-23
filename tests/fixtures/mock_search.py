import asyncio
from ddgs import DDGS
from starlette.concurrency import run_in_threadpool
from core.models import LinkedInSuggestion
from utils.helpers import clean_linkedin_url, extract_name_from_title, extract_title_from_snippet

def _run_ddg_sync(query: str, max_results: int) -> list:
    """Synchronous helper for DuckDuckGo search."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r)
    return results

async def execute_search_ddg(query: str, category: str, max_results: int = 20) -> list[LinkedInSuggestion]:
    """
    Executes a single search using DuckDuckGo asynchronously.
    Extracted from production core/search_engine.py to serve as a mock/test fallback.
    """
    suggestions = []
    try:
        results = await run_in_threadpool(_run_ddg_sync, query, max_results)
        for r in results:
            href = r.get("href", "")
            if "linkedin.com/in/" in href:
                title = r.get("title", "")
                snippet = r.get("body", "")
                
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
        # Rate limiting protection
        await asyncio.sleep(1.5)
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        
    return suggestions
