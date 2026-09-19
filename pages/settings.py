import streamlit as st
from services.data_manager import save_user_profile, get_user_profile
from services.ai import AIProvider

st.title("Settings & Profile")

profile = get_user_profile()

with st.expander("👤 Basic Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=profile.name if profile else "")
        university = st.text_input("University", value=profile.university if profile else "")
        degree = st.text_input("Degree", value=profile.degree if profile else "")
    with col2:
        graduation_year = st.text_input("Graduation Year", value=profile.graduation_year if profile else "")
        location = st.text_input("Location", value=profile.location if profile else "")
        current_status = st.text_input("Current Status", value=profile.current_status if profile else "")

with st.expander("💻 Technical Interests & Goals"):
    st.markdown("Enter comma-separated values (e.g. Python, React, AWS)")
    technical_interests = st.text_area("Technical Interests / Skills", value=profile.technical_interests if profile else "")
    target_job_titles = st.text_area("Target Job Titles", value=profile.target_job_titles if profile else "")
    target_companies = st.text_area("Target Companies", value=profile.target_companies if profile else "")
    target_industries = st.text_area("Target Industries", value=profile.target_industries if profile else "")

if st.button("Save Profile"):
    data = {
        "name": name,
        "university": university,
        "degree": degree,
        "graduation_year": graduation_year,
        "location": location,
        "current_status": current_status,
        "technical_interests": technical_interests,
        "target_job_titles": target_job_titles,
        "target_companies": target_companies,
        "target_industries": target_industries,
    }
    save_user_profile(data)
    st.success("Profile saved successfully!")

st.divider()

st.subheader("AI Configuration")
ai_provider = AIProvider()
if ai_provider.is_configured:
    st.success(f"AI Provider ({ai_provider.provider}) is configured and active.")
else:
    st.info("AI features are currently disabled. The deterministic networking assistant is fully functional. To enable AI, configure AI_API_KEY in the .env file.")
