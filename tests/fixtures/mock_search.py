"""Mock search fixtures for tests."""
from core.models import LinkedInSuggestion

def get_mock_suggestions() -> list[LinkedInSuggestion]:
    """Returns sample LinkedIn suggestions for testing without external API calls."""
    return [
        LinkedInSuggestion(
            name="Alex Rivera",
            title="Senior Staff Engineer",
            url="https://linkedin.com/in/alex-rivera-sample",
            snippet="Building distributed systems and cloud architectures at scale.",
            category="Same Role",
            action="Connect"
        ),
        LinkedInSuggestion(
            name="Morgan Vance",
            title="Technical Recruiter",
            url="https://linkedin.com/in/morgan-vance-sample",
            snippet="Recruiting top engineering talent across tech teams.",
            category="Recruiter / Talent",
            action="Connect"
        ),
        LinkedInSuggestion(
            name="Jordan Lee",
            title="VP of AI Engineering",
            url="https://linkedin.com/in/jordan-lee-sample",
            snippet="Leading AI/ML infrastructure initiatives.",
            category="Thought Leader",
            action="Follow"
        )
    ]
