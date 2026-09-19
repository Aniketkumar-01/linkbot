import streamlit as st
from services.discovery import discover_candidates
from services.csv_handler import import_csv

st.title("Discover Candidates")

tab1, tab2 = st.tabs(["Auto-Discover", "Bulk Import (CSV)"])

with tab1:
    st.markdown("### 🚀 Auto-Discover Connections")
    st.markdown("We will automatically search the web for public LinkedIn profiles that match the **Target Job Titles** and **Skills** you set in your Settings profile.")
    
    if st.button("✨ Find People to Connect With", type="primary"):
        with st.spinner("Scouring the web for the best matches... This may take a minute."):
            result = discover_candidates()
            
            if "error" in result:
                st.error(result["error"])
            else:
                count = result.get("count", 0)
                st.success(f"Successfully discovered and analyzed {count} new candidates!")
                st.info("Head over to the **Candidates List** to see their scores, or the **Networking Tracker** to start your outreach.")

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
