from pydantic import BaseModel, Field

class JobPosting(BaseModel):
    title: str
    min_salary: int = Field(None, alias="Min Salary")
    max_salary: int = Field(None, alias="Max Salary")
    location: str
    remote: str
    hybrid: str
    equity: str
    years_experience: int = Field(..., alias="Years Experience")
