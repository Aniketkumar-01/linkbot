import re
from urllib.parse import urlparse, urlunparse

def clean_linkedin_url(url: str) -> str:
    """
    Cleans a LinkedIn URL by removing query parameters and trailing slashes.
    Ensures it's a valid linkedin.com/in/ URL.
    """
    parsed = urlparse(url)
    if "linkedin.com" not in parsed.netloc:
        return url
    
    # Reconstruct URL without query params or fragments
    clean_path = parsed.path.rstrip('/')
    cleaned_url = urlunparse((parsed.scheme, parsed.netloc, clean_path, '', '', ''))
    return cleaned_url

def extract_name_from_title(title: str) -> str:
    """
    Extracts the person's name from a search result title.
    Usually looks like "John Doe - Software Engineer - Google | LinkedIn"
    """
    # Split by common separators
    parts = re.split(r'\s*[-|–—]\s*', title)
    if parts:
        name = parts[0].strip()
        # Remove "LinkedIn" if it's somehow in the name part
        name = name.replace("LinkedIn", "").strip()
        return name
    return "Unknown"

def extract_title_from_snippet(snippet: str) -> str:
    """
    Attempts to extract a professional title from the search snippet if not available in title.
    """
    # Simple heuristic: first line or before the first period
    parts = snippet.split('.')
    if parts:
        return parts[0].strip()
    return "LinkedIn Member"

def is_valid_github_url(url: str) -> bool:
    """Checks if a string is a valid GitHub profile URL, protecting against SSRF."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False
            
        # Defense-in-depth: Reject if any @ userinfo is present
        if '@' in parsed.netloc:
            return False
            
        # Reject raw IP addresses (Security Auditor check)
        # urlparse hostname handles stripping ports
        if parsed.hostname and re.match(r'^\d+\.\d+\.\d+\.\d+$', parsed.hostname):
            return False
            
        if parsed.hostname not in ('github.com', 'www.github.com'):
            return False
        
        path_parts = parsed.path.strip('/').split('/')
        if not path_parts or len(path_parts) > 1:
            return False
            
        username = path_parts[0]
        # GitHub username validation: alphanumeric and hyphens, no consecutive hyphens
        if not re.match(r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', username):
            return False
            
        return True
    except Exception:
        return False
