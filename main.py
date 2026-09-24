import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.resume_parser import process_resume
from core.github_scraper import scrape_github_profile
from core.profile_analyzer import analyze_profile_with_gemini
from core.search_engine import search_for_connections
from core.result_ranker import rank_and_score_results
from utils.helpers import is_valid_github_url, clean_linkedin_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global client holder
class AppState:
    http_client: Optional[httpx.AsyncClient] = None

def get_http_client() -> httpx.AsyncClient:
    """Returns the shared AsyncClient, creating one if not yet initialized."""
    if AppState.http_client is None or AppState.http_client.is_closed:
        AppState.http_client = httpx.AsyncClient(timeout=15.0)
    return AppState.http_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize a shared AsyncClient for connection pooling
    AppState.http_client = httpx.AsyncClient(timeout=15.0)
    yield
    if AppState.http_client and not AppState.http_client.is_closed:
        await AppState.http_client.aclose()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LinkBot API", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception):
    return FileResponse("static/404.html", status_code=404)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/api/analyze")
@limiter.limit("10/minute")
async def analyze_profile(
    request: Request,
    gemini_key: str = Form(...),
    serper_key: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
    github_url: Optional[str] = Form(None),
    bio_text: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
):
    gemini_key = (gemini_key or "").strip()
    if not gemini_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is required")

    serper_key = serper_key.strip() if serper_key else None
    http_client = get_http_client()

    extracted_text_parts = []

    if resume_file:
        if resume_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
            
        resume_file.file.seek(0, 2)
        file_size = resume_file.file.tell()
        resume_file.file.seek(0)
        
        if file_size > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB.")

        try:
            extracted_text = process_resume(resume_file.file)
            if extracted_text:
                extracted_text_parts.append(extracted_text)
        except Exception:
            logger.exception("Failed to process resume upload.")
            raise HTTPException(status_code=400, detail="Failed to process resume file.")

    if github_url:
        github_url = github_url.strip()
        if len(github_url) > 200:
            raise HTTPException(status_code=400, detail="GitHub URL is too long.")
        if is_valid_github_url(github_url):
            try:
                github_text = await scrape_github_profile(github_url, http_client)
                if github_text:
                    extracted_text_parts.append(github_text)
            except Exception:
                logger.exception("Failed to scrape GitHub profile.")
                raise HTTPException(status_code=400, detail="Failed to retrieve GitHub profile.")
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    if bio_text:
        bio_text = bio_text.strip()
        if len(bio_text) > 10000:
            raise HTTPException(status_code=400, detail="Bio text is too long (max 10,000 characters).")
        if bio_text:
            extracted_text_parts.append(f"Professional Summary / Bio: {bio_text}")

    if linkedin_url:
        linkedin_url = clean_linkedin_url(linkedin_url.strip())
        if len(linkedin_url) > 300:
            raise HTTPException(status_code=400, detail="LinkedIn URL is too long.")

    if not extracted_text_parts:
        raise HTTPException(
            status_code=400,
            detail="Please provide a resume, GitHub URL, or professional summary/bio."
        )

    extracted_text = "\n\n---\n\n".join(extracted_text_parts)

    try:
        # Step 1: Analyze Profile
        user_profile = await analyze_profile_with_gemini(extracted_text, gemini_key)
            
        if not user_profile:
            raise HTTPException(status_code=500, detail="Failed to analyze profile with Gemini.")

        # Attach source URLs if provided
        if linkedin_url and not user_profile.linkedin_url:
            user_profile.linkedin_url = linkedin_url
        if github_url and not user_profile.github_url:
            user_profile.github_url = github_url

        final_results = []
        if serper_key:
            # Step 2: Search LinkedIn
            raw_suggestions = await search_for_connections(
                user_profile,
                http_client,
                serper_api_key=serper_key,
                progress_callback=None
            )

            # Step 3: Rank Results
            final_results = await rank_and_score_results(
                user_profile,
                raw_suggestions,
                http_client,
                gemini_key
            )
        
        # Serialize and return
        return {
            "profile": user_profile.model_dump() if hasattr(user_profile, "model_dump") else user_profile.__dict__,
            "suggestions": [s.model_dump() if hasattr(s, "model_dump") else s.__dict__ for s in final_results]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Internal Server Error during profile analysis pipeline.")
        error_msg = str(e).lower()
        if "api_key" in error_msg or "403" in error_msg or "permission" in error_msg or "invalid argument" in error_msg or "not valid" in error_msg or "unauthorized" in error_msg:
            friendly_message = "It looks like your Gemini API key might be invalid or expired. Please check your API Settings."
        elif "quota" in error_msg or "429" in error_msg or "exhausted" in error_msg:
            friendly_message = "Your AI service quota has been exceeded. Please check your API account."
        elif "json" in error_msg or "validation" in error_msg or "parse" in error_msg:
            friendly_message = "We couldn't process the input data. Please make sure your URLs or files are valid."
        else:
            friendly_message = "An internal error occurred while analyzing your profile. Please check your API key and try again in a moment."
            
        raise HTTPException(status_code=500, detail=friendly_message)
