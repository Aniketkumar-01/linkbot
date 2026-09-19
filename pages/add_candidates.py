import streamlit as st
from services.data_manager import add_candidate
from services.scoring import calculate_deterministic_score
from services.csv_handler import import_csv

st.title("Add Candidates")

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Paste Text", "CSV Import"])

with tab1:
    st.subheader("Add Candidate Manually")
    with st.form("manual_candidate_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name*")
            linkedin_url = st.text_input("LinkedIn URL*")
            headline = st.text_input("Headline")
            company = st.text_input("Company")
            job_title = st.text_input("Job Title")
        with col2:
            location = st.text_input("Location")
            education = st.text_input("Education")
            skills_input = st.text_input("Skills (comma-separated)")
            mutual_connections = st.number_input("Mutual Connections", min_value=0, step=1)
        
        about = st.text_area("About / Bio")
        experience = st.text_area("Experience")
        
        submit_btn = st.form_submit_button("Add Candidate")
        
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
                else:
                    st.error("Candidate with this LinkedIn URL might already exist.")

with tab2:
    st.subheader("Paste Profile Information")
    st.markdown("*(Future AI implementation can extract structure from pasted text. Currently, please use Manual Entry or CSV)*")
    pasted_text = st.text_area("Paste text here", height=200)
    if st.button("Parse (Not implemented yet)"):
        st.warning("Feature requires AI parsing to map unstructured text to fields. Please use manual entry or CSV for now.")

with tab3:
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
