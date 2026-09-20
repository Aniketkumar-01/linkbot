# LinkBot 🔗

LinkBot is a free, AI-powered Streamlit web application that analyzes your resume or GitHub profile to find relevant professionals you should connect with or follow on LinkedIn.

## Features
- **Intelligent Profile Analysis**: Uses Google Gemini API to extract your skills, titles, and experience from a PDF resume or GitHub profile.
- **Automated Discovery**: Uses DuckDuckGo search (or Serper.dev) to find relevant LinkedIn profiles without scraping LinkedIn directly.
- **Smart Categorization**: Groups suggestions into categories like "Same Role", "Recruiters", "Thought Leaders", and "Alumni".
- **Completely Free**: No paid APIs required (Gemini has a generous free tier, DuckDuckGo is free).
- **Privacy First**: No LinkedIn login required. Does not store your resume.

## Setup Instructions

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

### Deployment (Streamlit Community Cloud)

1. Push your code to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select your repository.
4. Set the main file path to `app.py`.
5. (Optional) In the advanced settings, add your API keys to the Secrets:
   ```toml
   GEMINI_API_KEY = "your-google-gemini-key"
   SERPER_API_KEY = "your-optional-serper-key"
   ```
6. Click Deploy!

## API Keys
- **Google Gemini API**: Get a free key at [Google AI Studio](https://aistudio.google.com/). Required for profile analysis.
- **Serper.dev API (Optional)**: Get 2,500 free queries at [Serper.dev](https://serper.dev/). Recommended for higher-quality search results.

## Limitations & Disclaimer
- This app does **not** auto-connect or auto-follow on LinkedIn, as that violates their Terms of Service and can result in account bans. It provides you with direct links to manually review and connect.
- DuckDuckGo search limits may apply if you run the app continuously in a loop.
