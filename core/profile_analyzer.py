import json
import streamlit as st
from google import genai
from pydantic import ValidationError
from .models import UserProfile
from utils.constants import COMMON_SKILLS

def analyze_profile_with_gemini(text: str, api_key: str) -> UserProfile:
    """
    Uses Gemini to extract structured data from raw resume/GitHub text.
    """
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert career advisor and technical recruiter.
    Extract the following information from the provided text (which could be a resume and/or GitHub profile summary).
    
    Return ONLY a valid JSON object matching this structure exactly (do not wrap in markdown ```json blocks):
    {{
        "name": "Full Name",
        "headline": "A concise professional headline summarizing their expertise (e.g. 'Senior ML Engineer | Python | AWS')",
        "skills": ["Skill 1", "Skill 2"], (Focus on technical and hard skills, max 15)
        "job_titles": ["Title 1", "Title 2"], (Actual job titles they have held)
        "industries": ["Industry 1", "Industry 2"],
        "experience_years": 5, (Integer estimate of total years of professional experience)
        "education": ["Degree - Institution"],
        "location": "City, Country or Remote",
        "interests": ["Interest 1", "Interest 2"]
    }}
    
    If any field cannot be determined, provide an empty list for arrays, 0 for integers, and "" for strings.
    
    Text to analyze:
    {text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        # Clean potential markdown wrapping if the model ignores the instruction
        raw_json = response.text.strip()
        if raw_json.startswith("```json"):
            raw_json = raw_json[7:]
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]
            
        data = json.loads(raw_json)
        return UserProfile(**data)
        
    except Exception as e:
        st.toast(f"Gemini analysis failed, using fallback: {e}")
        # Fallback to basic extraction
        return fallback_extraction(text)

def fallback_extraction(text: str) -> UserProfile:
    """
    Basic keyword-based extraction if Gemini is unavailable or fails.
    """
    # Extremely basic fallback logic
    found_skills = [skill for skill in COMMON_SKILLS if skill.lower() in text.lower()]
    
    return UserProfile(
        name="User (Fallback Extraction)",
        headline="Software Professional",
        skills=found_skills,
        experience_years=0
    )
