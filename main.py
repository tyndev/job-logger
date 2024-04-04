from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
import httpx
import os


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI(title="Personal Job Posting Parser and Tracker", version="1.0")


async def fetch_job_posting(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        return response.text


def extract_relevant_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    # Get text
    text = soup.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

async def send_to_openai(clean_text: str) -> str | None:
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {'role': 'user', 'content': f"Find the following values from the job posting:Job Title, Min Salary (as an int), Max Salary (as an int), Location (as a str), Remote (yes/no/unknown), Hybrid (yes/no/unknown), Equity (yes/no/unknown), Years Experience (int)\n\n Job posting: {clean_text}\n\n Return only the found values as a csv."}
        ],
        temperature=0.7
    )
    print(clean_text)
    #TODO: impliment json? https://platform.openai.com/docs/guides/text-generation/json-mode
    
    return response.choices[0].message.content

async def parse_job_posting(url: str) -> str | None:
    job_posting_html = await fetch_job_posting(url)
    clean_text = extract_relevant_text(job_posting_html)
    parsed_data = await send_to_openai(clean_text)  
    return parsed_data


@app.post("/parse-job-posting/")
async def parse_job_posting_route(url: str):
    try:
        parsed_data = await parse_job_posting(url)
        return parsed_data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))