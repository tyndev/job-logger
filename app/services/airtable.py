import logging 
import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from app.models.job_posting import JobPosting

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Applications"  

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json",
}

async def insert_job_posting(job_posting: JobPosting):

    fields_data = job_posting.model_dump(by_alias=True, exclude_none=True)
    payload = {"records": [{"fields": fields_data}]}

    logging.info(f"Sending payload to Airtable: {payload}")
    
    airtable_url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    async with httpx.AsyncClient() as client:
        response = await client.post(airtable_url, json=payload, headers=headers)
        response.raise_for_status()  # TODO: handle errors appropriately
        return response.json()

# Example usage:
# job_posting = JobPosting(title="Software Engineer", company="Example Inc.", min_salary=50000, max_salary=100000, location="Remote", years_experience=2)
# await insert_job_posting(job_posting)

