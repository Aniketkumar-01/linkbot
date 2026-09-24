# LinkBot 🔗

LinkBot is a fast, AI-powered web application that analyzes your resume, GitHub profile, or bio to identify and recommend relevant professionals to connect with or follow on LinkedIn.

## ✨ Features
- **Intelligent Profile Analysis**: Leverages Google Gemini to extract your skills, titles, experience, and background from a PDF resume, GitHub profile, or bio text.
- **Automated LinkedIn Discovery**: Uses Serper.dev (Google Search API) to find real, relevant LinkedIn profiles without scraping LinkedIn directly.
- **Concurrent Search Execution**: Orchestrates multi-category discovery (Same Role, Industry Peers, Recruiters, Thought Leaders, Alumni) in parallel for ultra-fast results.
- **Smart Connection Actions**: Uses Gemini to analyze candidates and recommend whether to "Connect" (peers, hiring managers, recruiters) or "Follow" (industry leaders, executives).
- **Stateless & Privacy-First (BYOK)**: Bring Your Own Key architecture. No logins, no database, no stored resumes or keys.

## 🛠️ Tech Stack
- **Backend**: FastAPI, Uvicorn, Pydantic v2, SlowAPI (rate limiting), HTTPX (async HTTP client), pdfplumber.
- **Frontend**: Vanilla JavaScript, Tailwind CSS, Google Fonts & Material Symbols.
- **AI / APIs**: Google Gemini API (`google-genai`), Serper.dev API, GitHub REST API.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API key (free at [Google AI Studio](https://aistudio.google.com/))
- (Optional) A Serper.dev API key for live LinkedIn profile discovery (free tier available at [Serper.dev](https://serper.dev/))

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/Aniketkumar-01/linkbot.git
cd linkbot

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Locally
```bash
uvicorn main:app --reload --port 8000
```
Open your browser and navigate to `http://localhost:8000`.

## 🌐 Deployment (Render)

LinkBot is configured for deployment on [Render](https://render.com) using `render.yaml`:
1. Push your repository to GitHub.
2. Link your repository in Render as a Web Service.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔒 Privacy & Safety
- **No LinkedIn Credentials**: LinkBot never asks for or stores your LinkedIn credentials.
- **Compliance**: Does not scrape LinkedIn directly or automate actions (connecting/messaging) on LinkedIn, keeping your account safe from Terms of Service violations.
- **Zero Retention**: Uploaded resumes and API keys are processed transiently in memory and never persisted to disk or databases.

## 🧪 Running Tests
```bash
pytest
```
