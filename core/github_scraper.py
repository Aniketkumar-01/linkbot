import httpx
import re
from urllib.parse import urlparse

def extract_github_username(url: str) -> str:
    """Extracts username from a GitHub URL."""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    if path_parts:
        return path_parts[0]
    return ""

async def scrape_github_profile(github_url: str, client: httpx.AsyncClient) -> str:
    """
    Fetches GitHub profile and top repositories using the GitHub REST API asynchronously.
    Returns a text summary that can be fed to Gemini for analysis.
    """
    username = extract_github_username(github_url)
    if not username:
        return "Invalid GitHub URL."

    try:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "LinkBot-Networking-App"
        }
        
        # 1. Get user profile using shared client
        user_resp = await client.get(f"https://api.github.com/users/{username}", headers=headers)
        if user_resp.status_code != 200:
            return f"Could not access GitHub profile. Status: {user_resp.status_code}"
            
        user_data = user_resp.json()
        
        summary = []
        if user_data.get('name'):
            summary.append(f"Name: {user_data.get('name')}")
        if user_data.get('bio'):
            summary.append(f"Bio: {user_data.get('bio')}")
        if user_data.get('company'):
            summary.append(f"Company: {user_data.get('company')}")
        if user_data.get('location'):
            summary.append(f"Location: {user_data.get('location')}")
            
        # 2. Get repositories
        repos_resp = await client.get(f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10", headers=headers)
        
        if repos_resp.status_code == 200:
            repos_data = repos_resp.json()
            if repos_data:
                summary.append("\nRecent Repositories and Technologies:")
                for repo in repos_data:
                    # Skip forks if we want only original work, but let's include all for broader skill mapping
                    repo_info = f"- {repo.get('name')}"
                    if repo.get('language'):
                        repo_info += f" ({repo.get('language')})"
                    if repo.get('description'):
                        repo_info += f": {repo.get('description')}"
                        
                    summary.append(repo_info)
                    
        return "\n".join(summary)
            
    except httpx.TimeoutException:
        return "Error fetching GitHub profile: Timeout"
    except Exception as e:
        return f"Error fetching GitHub profile: {str(e)}"
