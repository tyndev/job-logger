from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
import instructor 

from app.models.job_posting import JobPosting

load_dotenv()

client = instructor.from_openai(AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")))

async def send_to_openai(clean_text: str) -> JobPosting:
    response = await client.chat.completions.create(
        model='gpt-4',
        messages=[
            {'role': 'user', 'content': f"Summarize the following job posting into one short sentence. Determine the most important keywords that applicants should include in their resume. Then classify the following job description and include your summary as the 'Job Description Summary' and your keywords as 'Keywords'. Job Posting: {clean_text}"}
        ],
        temperature=0.7,
        response_model=JobPosting
    )   
    return response
