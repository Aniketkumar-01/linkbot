import pdfplumber
import re

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text from an uploaded PDF file object using pdfplumber.
    """
    full_text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                # Extract text preserving layout as much as possible
                text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if text:
                    full_text += text + "\n\n"
    except Exception as e:
        # Fallback if there's an issue with pdfplumber
        import streamlit as st
        st.toast(f"Error extracting PDF: {e}")
        pass
    
    return full_text

def clean_extracted_text(text: str) -> str:
    """
    Basic cleaning of extracted text.
    """
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def process_resume(pdf_file) -> str:
    """
    Main entry point for processing a resume file.
    Returns the cleaned raw text.
    """
    raw_text = extract_text_from_pdf(pdf_file)
    cleaned_text = clean_extracted_text(raw_text)
    return cleaned_text
