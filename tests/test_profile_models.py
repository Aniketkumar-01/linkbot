import pytest
from pydantic import ValidationError
from core.models import UserProfile, LinkedInSuggestion

def test_user_profile_default_values():
    profile = UserProfile()
    assert profile.name == ""
    assert profile.skills == []
    assert profile.experience_years == 0

def test_linkedin_suggestion_connect_message_limit():
    long_msg = "A" * 400
    suggestion = LinkedInSuggestion(
        name="Jane",
        title="Engineer",
        url="https://linkedin.com/in/jane",
        snippet="Snippet",
        connect_message=long_msg
    )
    assert len(suggestion.connect_message) == 300
    assert suggestion.connect_message.endswith("...")

def test_linkedin_suggestion_validation_error():
    with pytest.raises(ValidationError):
        LinkedInSuggestion(
            name="Jane",
            # missing title, url, snippet which are required
        )
