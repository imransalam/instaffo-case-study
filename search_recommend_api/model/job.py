from pydantic import BaseModel
from typing import Optional, List

class Job(BaseModel):
    """
    Data model for a Job.
    
    Attributes
    ----------
    top_skills : List[str]
        A list of top skills required for the job.
    other_skills : List[str]
        A list of optional skills required for the job.
    seniorities : List[str]
        A list of seniority levels required for the job.
    max_salary : int
        The maximum salary offered for the job.
    """
    top_skills : Optional[List[str]]
    other_skills : Optional[List[str]]
    seniorities : Optional[List[str]]
    max_salary : Optional[int]