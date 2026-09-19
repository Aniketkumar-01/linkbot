import streamlit as st
from services.data_manager import save_user_profile, get_user_profile
from services.ai import AIProvider
from services.csv_handler import export_candidates_to_csv

st.title("Settings & Profile")

# Initialize session state for extracted profile
if "extracted_profile" not in st.session_state:
    st.session_state.extracted_profile = {}

st.markdown("### 1. Auto-Extract Profile from Resume")
extract_text = st.text_area("Paste your Resume / LinkedIn Profile here", height=150, help="We'll extract your skills and target roles automatically.")
if st.button("✨ Extract My Profile via AI"):
    if not extract_text.strip():
        st.error("Please paste some text.")
    else:
        with st.spinner("Analyzing your profile..."):
            ai_provider = AIProvider()
            result = ai_provider.extract_user_profile(extract_text)
            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.extracted_profile = result
                st.success("Profile extracted! Review and save below.")
                st.rerun()

st.divider()
st.markdown("### 2. Verify & Save Profile")

profile = get_user_profile()
p_data = st.session_state.extracted_profile

def get_val(key, default_attr):
    if key in p_data:
        val = p_data[key]
        return ", ".join(val) if isinstance(val, list) else str(val)
    return getattr(profile, default_attr) if profile else ""

with st.expander("👤 Basic Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=get_val("name", "name"))
        university = st.text_input("University", value=get_val("university", "university"))
        degree = st.text_input("Degree", value=get_val("degree", "degree"))
    with col2:
        graduation_year = st.text_input("Graduation Year", value=get_val("graduation_year", "graduation_year"))
        location = st.text_input("Location", value=get_val("location", "location"))
        current_status = st.text_input("Current Status", value=get_val("current_status", "current_status"))

with st.expander("💻 Technical Interests & Goals"):
    st.markdown("Enter comma-separated values (e.g. Python, React, AWS)")
    technical_interests = st.text_area("Technical Interests / Skills", value=get_val("technical_interests", "technical_interests"))
    target_job_titles = st.text_area("Target Job Titles", value=get_val("target_job_titles", "target_job_titles"))
    target_companies = st.text_area("Target Companies", value=get_val("target_companies", "target_companies"))
    target_industries = st.text_area("Target Industries", value=get_val("target_industries", "target_industries"))

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
    st.session_state.extracted_profile = {} # Clear it after saving

st.divider()

st.subheader("AI Configuration")
ai_provider = AIProvider()
if ai_provider.is_configured:
    st.success(f"AI Provider ({ai_provider.provider}) is configured and active.")
else:
    st.info("AI features are currently disabled. Configure AI_API_KEY in your .env file.")

st.divider()

st.subheader("Data Management")
st.markdown("Export your networking data to CSV for backup.")
if st.button("Export Candidates to CSV"):
    df = export_candidates_to_csv()
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='candidates_export.csv',
            mime='text/csv',
        )
    else:
        st.warning("No candidates to export.")
