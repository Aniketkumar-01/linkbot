# LinkedIn Networking Assistant

A personal networking assistant built with Python and Streamlit. This tool helps you organize, score, and prioritize LinkedIn profiles to decide whether to Connect, Follow, or Ignore them. 

**Important:** This application strictly respects LinkedIn's Terms of Service by **NOT** automating any interactions. It acts as an offline-first CRM for your networking efforts.

## Features
- **Zero-Cost:** Runs locally using SQLite, Streamlit, and Python. No paid APIs or databases required.
- **Deterministic Scoring:** Transparently scores candidates based on your configured profile preferences (role, skills, company, education).
- **Networking Tracker:** A Kanban-style board to track the status of your networking efforts (New -> Reviewed -> Follow -> Connect -> Messaged).
- **Message Generator:** Generates connection messages.
- **CSV Support:** Import and export your candidates to backup your data.
- **Optional AI:** The app runs perfectly offline. Optionally, add an `AI_API_KEY` in your `.env` for AI-powered messaging.

## Tech Stack
- **Frontend / UI:** Streamlit
- **Backend / Logic:** Python
- **Database:** SQLite (managed via SQLAlchemy)
- **Data Manipulation:** Pandas

## Project Structure
```
linkbot/
├── app.py                      # Main Streamlit application entry point
├── database/                   # SQLite database configuration and models
├── pages/                      # Streamlit UI pages (Dashboard, Settings, Candidates, etc.)
├── services/                   # Core business logic (Scoring, AI, CSV Handling, DB operations)
├── utils/                      # Constants and helpers
├── tests/                      # Pytest suite
├── seed_demo_data.py           # Script to populate the DB with demo data
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## Running Locally

1. **Clone the repository** (if applicable) and navigate to the folder:
   ```bash
   cd linkbot
   ```

2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Seed Demo Data (Optional):**
   ```bash
   python seed_demo_data.py
   ```

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Optional AI Configuration
To enable AI message generation, create a `.env` file from the `.env.example`:
```
AI_PROVIDER=openai  # or google-genai, ollama, etc.
AI_API_KEY=your_api_key_here
```
*If left blank, the app gracefully degrades and remains 100% functional with deterministic scoring and template messages.*

## Deployment
You can deploy this application for free using **Streamlit Community Cloud**:
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select this repository.
4. Set the main file path as `app.py`.
5. Click **Deploy!**

**Note on Data Persistence:** Streamlit Community Cloud environments are ephemeral. The local `networking.db` SQLite file might be reset on app reboots. Be sure to use the **Data Management** page to export your candidates to CSV regularly!

## Privacy and LinkedIn Limitations
This app **does not require your LinkedIn credentials** and **does not automate any LinkedIn actions**. You remain entirely in control. Use the generated messages and profile links to manually perform outreach.
