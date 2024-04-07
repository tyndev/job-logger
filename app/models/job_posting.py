from pydantic import BaseModel, Field
import enum


class JobPosting(BaseModel):
    company: str = Field(..., alias="Company")
    title: str = Field(..., alias="Job Title")
    min_salary: int = Field(None, alias="Min Salary")
    max_salary: int = Field(None, alias="Max Salary")
    location: str = Field(None, alias="Location")
    remote: str = Field(None, alias="Remote")
    hybrid: str = Field(None, alias="Hybrid")
    equity: str = Field(None, alias="Equity")
    keywords: str = Field(None, alias="Keywords")
    job_description_summary: str = Field(None, alias="Job Description Summary")
    years_experience: int = Field(None, alias="Years Experience")
    posting_link: str = Field(None, alias="Posting Link")


# TODO: Incorporate teh Below Labels 

class OfficeLocationLabels(str, enum.Enum):
    SF = "sf"
    LONDON = "london"
    REMOTE = "remote"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"
    OTHER = "other"
    
class BenefitLabels(str, enum.Enum):
    EQUITY = "equity"
    MATCH_401K = "match_401k"
    HEALTH_INSURANCE = "health_insurance"
    PARENTAL_LEAVE = "parental_leave"
    FERTILITY = "fertility"
    LUNCH = "lunch"
    DINNER = "dinner"