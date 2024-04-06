import httpx
import logging

from fastapi import FastAPI, HTTPException

from .utils.text_extraction import fetch_job_posting, extract_relevant_text
from .services.openai_services import send_to_openai
from .models.job_posting import JobPosting
from .services.airtable import insert_job_posting

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="Personal Job Posting Parser and Tracker", version="1.0")


async def parse_job_posting(url: str) -> JobPosting:
    job_posting_html = await fetch_job_posting(url)
    clean_text = extract_relevant_text(job_posting_html)
    parsed_data = await send_to_openai(clean_text)  
    return parsed_data


# @app.post("/job-posting/", response_model=JobPosting)
@app.post("/job-posting/")
async def parse_job_posting_route(url: str):
    try:
        parsed_data = await parse_job_posting(url)
        saved_record = await insert_job_posting(parsed_data)
        return {"message": "Job posting parsed and saved successfully", "data": saved_record}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))