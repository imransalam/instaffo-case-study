from pydantic import BaseModel, Field
from typing import Optional

class Filters(BaseModel):
    """
    Data model for filters.
    
    Attributes
    ----------
    top_skills_match : Optional[bool]
        A boolean indicating if we want to use the top skills match.
    seniority_match : Optional[bool]
        A boolean indicating if we want to use the seniority match.
    salary_match : Optional[bool]
        A boolean indicating if we want to use the salary expectation match.
    """
    top_skills_match: Optional[bool] = Field(False, description="Indicates whether to use the top skills match filter.")
    seniority_match: Optional[bool] = Field(False, description="Indicates whether to use the seniority match filter.")
    salary_match: Optional[bool] = Field(False, description="Indicates whether to use the salary match filter.")