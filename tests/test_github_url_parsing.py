import pytest
from utils.helpers import is_valid_github_url

def test_valid_github_urls():
    assert is_valid_github_url("https://github.com/aniket")
    assert is_valid_github_url("http://github.com/aniket")
    assert is_valid_github_url("https://www.github.com/aniket")
    assert is_valid_github_url("https://github.com/aniket/")
    assert is_valid_github_url("https://github.com/Aniket-123")

def test_invalid_github_urls():
    # SSRF / missing scheme
    assert not is_valid_github_url("github.com/aniket")
    assert not is_valid_github_url("ftp://github.com/aniket")
    
    # SSRF / Dangerous IPs masking as github
    assert not is_valid_github_url("https://github.com@127.0.0.1/aniket")
    assert not is_valid_github_url("https://github.com@localhost/aniket")
    assert not is_valid_github_url("https://github.com@169.254.169.254/aniket")
    assert not is_valid_github_url("https://127.0.0.1/aniket")
    
    # Wrong domain
    assert not is_valid_github_url("https://gitlab.com/aniket")
    assert not is_valid_github_url("https://github.com.evil.com/aniket")
    
    # Path issues
    assert not is_valid_github_url("https://github.com/aniket/repo")
    assert not is_valid_github_url("https://github.com/")
    
    # Invalid username format
    assert not is_valid_github_url("https://github.com/-aniket")
    assert not is_valid_github_url("https://github.com/aniket-")
    assert not is_valid_github_url("https://github.com/an--iket")
