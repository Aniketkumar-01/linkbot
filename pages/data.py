import streamlit as st
import pandas as pd
from services.csv_handler import export_candidates_to_csv
import os

st.title("Data Management")

st.markdown("""
Manage your LinkedIn Networking Assistant data. 

**Important Note for Cloud Deployments**: If you are running this on Streamlit Community Cloud or a similar ephemeral environment, your SQLite database changes may not persist permanently. Please regularly export your data to CSV to back it up.
""")

st.subheader("Export Data")

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

st.subheader("Import Data")
st.markdown("Use the **Add Candidates** page -> **CSV Import** tab to upload candidates from a CSV file.")
