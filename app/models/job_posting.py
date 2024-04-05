from pydantic import BaseModel, Field
from typing import List
import enum


class JobPosting(BaseModel):
    title: str
    min_salary: int = Field(None, alias="Min Salary")
    max_salary: int = Field(None, alias="Max Salary")
    location: str
    remote: str
    hybrid: str
    equity: str
    years_experience: int = Field(..., alias="Years Experience")


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