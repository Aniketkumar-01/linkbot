import os
import logging
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import httpx

from core.resume_parser import process_resume
from core.github_scraper import scrape_github_profile
from core.profile_analyzer import analyze_profile_with_gemini
from core.search_engine import search_for_connections
from core.result_ranker import rank_and_score_results
from utils.helpers import is_valid_github_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global client holder
class AppState:
    http_client: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize a shared AsyncClient for connection pooling (Performance Optimization)
    AppState.http_client = httpx.AsyncClient(timeout=15.0)
    yield
    await AppState.http_client.aclose()

app = FastAPI(title="LinkBot API", lifespan=lifespan)

# Serve the static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/api/analyze")
async def analyze_profile(
    gemini_key: str = Form(...),
    serper_key: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
    github_url: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None)
):
    if not gemini_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is required")

    extracted_text_parts = []
    user_linkedin_url = ""

    if resume_file:
        try:
            extracted_text = process_resume(resume_file.file)
            extracted_text_parts.append(extracted_text)
        except Exception as e:
            logger.exception("Failed to process resume upload.")
            raise HTTPException(status_code=400, detail="Failed to process resume file.")

    if github_url:
        if is_valid_github_url(github_url):
            try:
                github_text = await scrape_github_profile(github_url, AppState.http_client)
                extracted_text_parts.append(github_text)
            except Exception as e:
                logger.exception("Failed to scrape GitHub profile.")
                raise HTTPException(status_code=400, detail="Failed to retrieve GitHub profile.")
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    if linkedin_url:
        user_linkedin_url = linkedin_url
        extracted_text_parts.append(f"My LinkedIn URL is: {linkedin_url}")

    if not extracted_text_parts:
        raise HTTPException(status_code=400, detail="Please provide a resume, GitHub URL, or LinkedIn URL.")

    extracted_text = "\n\n---\n\n".join(extracted_text_parts)

    try:
        # Step 1: Analyze Profile
        user_profile = await analyze_profile_with_gemini(extracted_text, gemini_key)
        if user_linkedin_url:
            user_profile.linkedin_url = user_linkedin_url
            
        if not user_profile:
            raise HTTPException(status_code=500, detail="Failed to analyze profile with Gemini.")

        # Step 2: Search LinkedIn
        raw_suggestions = await search_for_connections(
            user_profile,
            AppState.http_client,
            serper_api_key=serper_key,
            progress_callback=None
        )

        # Step 3: Rank Results
        final_results = await rank_and_score_results(user_profile, raw_suggestions, AppState.http_client, gemini_key)
        
        # Serialize and return
        return {
            "profile": user_profile.model_dump() if hasattr(user_profile, "model_dump") else user_profile.__dict__,
            "suggestions": [s.model_dump() if hasattr(s, "model_dump") else s.__dict__ for s in final_results]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Internal Server Error during profile analysis pipeline.")
        raise HTTPException(status_code=500, detail="An internal error occurred during analysis. Please try again.")
