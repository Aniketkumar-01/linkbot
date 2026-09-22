import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
from core.models import UserProfile, LinkedInSuggestion


@pytest.fixture
def mock_dependencies(mocker):
    return {
        "process_resume": mocker.patch("main.process_resume", return_value="Extracted resume text"),
        "scrape_github_profile": mocker.patch("main.scrape_github_profile", new_callable=AsyncMock, return_value="GitHub profile text"),
        "analyze_profile": mocker.patch("main.analyze_profile_with_gemini", new_callable=AsyncMock, return_value=UserProfile(name="Test User", skills=["Python"])),
        "search": mocker.patch("main.search_for_connections", new_callable=AsyncMock, return_value=[LinkedInSuggestion(name="Peer", title="Eng", url="https://linkedin.com/in/peer", snippet="")]),
        "rank": mocker.patch("main.rank_and_score_results", new_callable=AsyncMock, return_value=[LinkedInSuggestion(name="Peer", title="Eng", url="https://linkedin.com/in/peer", snippet="", relevance_score=90)])
    }

def test_analyze_profile_missing_gemini_key():
    with TestClient(app) as client:
        response = client.post("/api/analyze", data={"github_url": "https://github.com/test"})
        assert response.status_code == 400
        assert "Gemini API Key is required" in response.json()["detail"]

def test_analyze_profile_no_inputs():
    with TestClient(app) as client:
        response = client.post("/api/analyze", data={"gemini_key": "dummy_key"})
        assert response.status_code == 400
        assert "Please provide a resume, GitHub URL, or LinkedIn URL" in response.json()["detail"]

def test_analyze_profile_invalid_github_url():
    with TestClient(app) as client:
        response = client.post("/api/analyze", data={"gemini_key": "dummy_key", "github_url": "invalid_url"})
        assert response.status_code == 400
        assert "Invalid GitHub URL" in response.json()["detail"]

def test_analyze_profile_success(mock_dependencies):
    with TestClient(app) as client:
        response = client.post("/api/analyze", data={
            "gemini_key": "dummy_key",
            "github_url": "https://github.com/test",
            "linkedin_url": "https://linkedin.com/in/test"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "profile" in data
        assert data["profile"]["name"] == "Test User"
        assert "suggestions" in data
        assert len(data["suggestions"]) == 1
        assert data["suggestions"][0]["name"] == "Peer"
        
        # Ensure keys are not leaked in the response
        response_text = response.text
        assert "dummy_key" not in response_text

def test_analyze_profile_internal_error_is_safe(mock_dependencies):
    # Force an internal error
    mock_dependencies["analyze_profile"].side_effect = Exception("Super secret internal error")
    
    with TestClient(app) as client:
        response = client.post("/api/analyze", data={
            "gemini_key": "dummy_key",
            "github_url": "https://github.com/test"
        })
        
        assert response.status_code == 500
        assert "An internal error occurred" in response.json()["detail"]
        assert "Super secret internal error" not in response.text
