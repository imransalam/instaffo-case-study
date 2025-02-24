from search_recommend_api.router import (
    APIRouter, 
    JSONResponse, 
    Filters,
    traceback,
    ElasticsearchClient,
    RecommendationResponse,
    HTTPException,
    Depends,
    _log
)
from search_recommend_api.model.candidate import Candidate
from typing import List


# Initialize API router and Elasticsearch clients
router: APIRouter = APIRouter()
candidates_index: ElasticsearchClient = ElasticsearchClient("candidates")
jobs_index: ElasticsearchClient = ElasticsearchClient("jobs")

@router.get(
    "/candidate/{id}",
    response_model=Candidate,
    summary="To get the candidate details by an ID",
    responses={
        200: {"model": Candidate}, 
        500: {"description": "Internal Server Error"}, 
        422: {"description": "Validation Error"}
    }
)
async def _candidate(id: int) -> JSONResponse:
    """
    Gets candidate data based on the ID provided

    Parameters
    ----------
    id : int
        This is the candidate id from the ES index of candidates
    
    Returns
    -------
    JSONResponse
        JSON response containing the Candidate object.
    """
    try:
        _log(f"GET /candidate/{id}", format="info")
        candidate_object: dict = candidates_index.get_entity(id=id)
        response = Candidate(
            top_skills=candidate_object['top_skills'],
            other_skills=candidate_object['other_skills'],
            seniority=candidate_object['seniority'],
            salary_expectation=candidate_object['salary_expectation']
        )
        return response
    except Exception as e:
        _log(f"Internal Server Error: /candidate/{id}", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )
    
@router.get(
    "/candidate/{id}/recommendJobs",
    response_model=List[RecommendationResponse],
    summary="To get the top Jobs for a candidate based on the ID and filters provided",
    responses={
        200: {"model": List[RecommendationResponse]}, 
        500: {"description": "Internal Server Error"}, 
        422: {"description": "Validation Error"}
    }
)
async def _recommend_jobs(id: int,
                     filters: Filters=Depends()) -> JSONResponse:
    """
    Gets the top Jobs based on candidates ID and filters provided

    Parameters
    ----------
    id : int
        This is the candidate id from the ES index of candidates
    filters : Filters
       This is the filters object which contains the filters to be applied on the jobs
       The filters included are 
       1. seniority_match
       2. salary_match
       3. top_skills_match
    
    Returns
    -------
    JSONResponse
        JSON response containing the RecommendationResponse object.
    """
    try:
        _log(f"GET /candidate/{id}/recommendJobs", format="info")
        candidate_object: dict = candidates_index.get_entity(id=id)
        should_queries: list[dict] = jobs_index.build_should_queries(entity_data=candidate_object, 
                                                         filters_used=filters)
        response = jobs_index.search_with_bool_queries(should_queries=should_queries, 
                                                       return_source=False)
        final_response: list[RecommendationResponse] = jobs_index.get_recommendation_type_output(response=response)
        return final_response
    except ValueError as e:
        _log(f"Validation Error: Missing filters for /candidate/{id}/recommendJobs", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=422,
            detail="At least one of the filters (seniority_match, salary_match, top_skills_match) must be provided."
        )
    except Exception as e:
        _log(f"Internal Server Error: /candidate/{id}/recommendJobs", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )