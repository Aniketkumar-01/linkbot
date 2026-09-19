import streamlit as st
from services.data_manager import add_candidate
from services.scoring import calculate_deterministic_score
from services.csv_handler import import_csv
from services.ai import AIProvider

st.title("Add Candidates")

# Initialize session state for extracted data
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = {}

tab1, tab2 = st.tabs(["Single Candidate", "Bulk Import (CSV)"])

with tab1:
    st.subheader("1. Auto-Extract Data (Optional)")
    st.markdown("Paste a resume or LinkedIn profile text here. The AI will automatically extract the details and fill the form below.")
    
    extract_text = st.text_area("Paste Profile / Resume Text", height=150, help="Copy the entire text from a LinkedIn profile or resume and paste it here.")
    
    if st.button("✨ Extract Data via AI"):
        if not extract_text.strip():
            st.error("Please paste some text to extract.")
        else:
            with st.spinner("Extracting candidate details..."):
                ai_provider = AIProvider()
                result = ai_provider.extract_candidate_data(extract_text)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.extracted_data = result
                    st.success("Data extracted successfully! Please review the fields below.")
                    st.rerun()

    st.divider()
    
    st.subheader("2. Verify & Save Candidate")
    with st.form("manual_candidate_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name*", value=st.session_state.extracted_data.get("name", ""))
            linkedin_url = st.text_input("LinkedIn URL*", value=st.session_state.extracted_data.get("linkedin_url", ""))
            headline = st.text_input("Headline", value=st.session_state.extracted_data.get("headline", ""))
            company = st.text_input("Company", value=st.session_state.extracted_data.get("company", ""))
            job_title = st.text_input("Job Title", value=st.session_state.extracted_data.get("job_title", ""))
        with col2:
            location = st.text_input("Location", value=st.session_state.extracted_data.get("location", ""))
            education = st.text_input("Education", value=st.session_state.extracted_data.get("education", ""))
            
            skills_list = st.session_state.extracted_data.get("skills", [])
            skills_str = ", ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)
            skills_input = st.text_input("Skills (comma-separated)", value=skills_str)
            
            mutual_connections = st.number_input("Mutual Connections", min_value=0, step=1)
        
        about = st.text_area("About / Bio", value=st.session_state.extracted_data.get("about", ""))
        experience = st.text_area("Experience", value=st.session_state.extracted_data.get("experience", ""))
        
        submit_btn = st.form_submit_button("Save Candidate")
        
        if submit_btn:
            if not name or not linkedin_url:
                st.error("Name and LinkedIn URL are required.")
            else:
                data = {
                    "name": name,
                    "linkedin_url": linkedin_url,
                    "headline": headline,
                    "company": company,
                    "job_title": job_title,
                    "location": location,
                    "education": education,
                    "about": about,
                    "experience": experience,
                    "mutual_connections": mutual_connections
                }
                skills = [s.strip() for s in skills_input.split(",")] if skills_input else []
                cid = add_candidate(data, skills)
                if cid:
                    calculate_deterministic_score(cid)
                    st.success(f"Candidate {name} added and scored successfully!")
                    st.session_state.extracted_data = {} # Clear the form
                else:
                    st.error("Candidate with this LinkedIn URL might already exist.")

with tab2:
    st.subheader("CSV Import")
    st.markdown("Upload a CSV file containing candidate information. Required columns: `linkedin_url`.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        if st.button("Import CSV"):
            result = import_csv(uploaded_file)
            if "error" in result:
                st.error(f"Error importing CSV: {result['error']}")
            else:
                st.success(f"Imported {result['success']} candidates. Skipped {result['skipped']}.")
