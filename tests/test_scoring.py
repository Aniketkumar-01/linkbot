from core.result_ranker import calculate_fast_score
from core.models import UserProfile, LinkedInSuggestion

def test_calculate_fast_score():
    profile = UserProfile(
        job_titles=["Software Engineer"],
        skills=["Python", "AWS"],
        industries=["Technology"],
        location="New York"
    )
    
    # Highly relevant suggestion
    s1 = LinkedInSuggestion(
        name="Jane",
        title="Senior Software Engineer",
        url="https://linkedin.com/in/jane",
        snippet="Building scalable systems with Python and AWS in Technology sector in New York."
    )
    score1 = calculate_fast_score(profile, s1)
    
    # Irrelevant suggestion
    s2 = LinkedInSuggestion(
        name="Bob",
        title="Marketing Manager",
        url="https://linkedin.com/in/bob",
        snippet="SEO and content creation in Retail."
    )
    score2 = calculate_fast_score(profile, s2)
    
    assert score1 > score2
    assert score1 <= 1.0
