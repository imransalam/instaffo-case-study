from pydantic import BaseModel
from typing import Optional

class RecommendationResponse(BaseModel):
    """
    Output data model for a Candidate and Job recommendation.
    
    Attributes
    ----------
    id: int
        The id of the recommended candidate or job.
    relevance_score: float
        The relevance score of the recommended candidate or job.
    """
    id: Optional[int]
    relevance_score: Optional[float]