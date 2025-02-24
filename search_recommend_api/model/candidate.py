from pydantic import BaseModel
from typing import Optional, List

class Candidate(BaseModel):
    """
    Data model for a Candidate.
    
    Attributes
    ----------
    top_skills : List[str]
        A list of top skills by the candidate.
    other_skills : List[str]
        A list of optional skills by the candidate.
    seniority : str
        The seniority level of the candidate.
    salary_expectation : int
        The salary expected by the candidate.
    """
    top_skills : Optional[List[str]]
    other_skills : Optional[List[str]]
    seniority : Optional[str]
    salary_expectation : Optional[int]