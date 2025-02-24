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
from search_recommend_api.model.job import Job
from typing import List


# Initialize API router and Elasticsearch clients
router: APIRouter = APIRouter()
jobs_index: ElasticsearchClient = ElasticsearchClient("jobs")
candidates_index: ElasticsearchClient = ElasticsearchClient("candidates")

@router.get(
    "/job/{id}",
    response_model=Job,
    summary="To get the job details by an ID",
    responses={
        200: {"model": Job}, 
        500: {"description": "Internal Server Error"}, 
        422: {"description": "Validation Error"}
    }
)
async def _job(id: int) -> JSONResponse:
    """
    Gets job data based on the ID provided

    Parameters
    ----------
    id : int
        This is the job id from the ES index of jobs
    
    Returns
    -------
    JSONResponse
        JSON response containing the Job object.
    """
    try:
        _log(f"GET /job/{id}", format="info")
        jobs_object: dict = jobs_index.get_entity(id=id)
        response = Job(
            top_skills=jobs_object['top_skills'],
            other_skills=jobs_object['other_skills'],
            seniorities=jobs_object['seniorities'],
            max_salary=jobs_object['max_salary']
        )
        return response
    except Exception as e:
        _log(f"Internal Server Error: /job/{id}", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )
    
@router.get(
    "/job/{id}/recommendCandidates",
    response_model=List[RecommendationResponse],
    summary="To get the top Candidates for a job based on the ID and filters provided",
    responses={
        200: {"model": List[RecommendationResponse]}, 
        500: {"description": "Internal Server Error"}, 
        422: {"description": "Validation Error"}
    }
)
async def _recommend_candidates(id: int,
                     filters: Filters=Depends()) -> JSONResponse:
    """
    Gets the top Candidates based on Job ID and filters provided

    Parameters
    ----------
    id : int
        This is the job id from the ES index of jobs
    filters : Filters
       This is the filters object which contains the filters to be applied on the candidates
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
        _log(f"GET /job/{id}/recommendCandidates", format="info")
        jobs_object: dict = jobs_index.get_entity(id=id)
        should_queries: list[dict] = candidates_index.build_should_queries(entity_data=jobs_object, 
                                                         filters_used=filters)
        response = candidates_index.search_with_bool_queries(should_queries=should_queries, 
                                                       return_source=False)
        final_response: List[RecommendationResponse] = candidates_index.get_recommendation_type_output(response=response)
        return final_response
    except ValueError as e:
        _log(f"Validation Error: Missing filters for /job/{id}/recommendCandidates", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=422,
            detail="At least one of the filters (seniority_match, salary_match, top_skills_match) must be provided."
        )
    except Exception as e:
        _log(f"Internal Server Error: /job/{id}/recommendCandidates", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )