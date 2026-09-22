import pytest
from core.search_engine import generate_search_queries
from core.models import UserProfile
from utils.constants import CATEGORY_SAME_ROLE, CATEGORY_INDUSTRY_PEER, CATEGORY_RECRUITER

def test_generate_search_queries_normal_profile():
    profile = UserProfile(
        name="John",
        job_titles=["Software Engineer"],
        skills=["Python", "FastAPI", "React"],
        industries=["Technology"],
        location="San Francisco, CA",
        education=["BS Computer Science - Stanford"]
    )
    queries = generate_search_queries(profile)
    assert len(queries[CATEGORY_SAME_ROLE]) > 0
    assert "Software Engineer" in queries[CATEGORY_SAME_ROLE][0]
    assert "Python" in queries[CATEGORY_SAME_ROLE][0]
    assert "FastAPI" in queries[CATEGORY_SAME_ROLE][0]
    assert len(queries[CATEGORY_INDUSTRY_PEER]) > 0
    assert "Technology" in queries[CATEGORY_INDUSTRY_PEER][0]
    assert "San Francisco" in queries[CATEGORY_INDUSTRY_PEER][0]

def test_generate_search_queries_empty_profile():
    profile = UserProfile()
    queries = generate_search_queries(profile)
    assert len(queries[CATEGORY_SAME_ROLE]) == 0 # Cannot make same role query without >=2 skills
    assert len(queries[CATEGORY_INDUSTRY_PEER]) == 0 # Needs industry and location
    assert len(queries[CATEGORY_RECRUITER]) > 0
    assert "Tech" in queries[CATEGORY_RECRUITER][0] # Default fallback
