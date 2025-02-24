import traceback
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from search_recommend_api.logger import _log

# Initialize API router and Elasticsearch clients
router: APIRouter = APIRouter()

@router.get(
    "/", 
    response_model=dict, 
    summary="Index Endpoint",
    responses={
        200: {"description": "Successful response from the root endpoint"},
        500: {"description": "Internal Server Error"}
    }
)
async def _index(request: Request) -> JSONResponse:
    """
    Handle requests to the root endpoint of the API.

    Parameters
    ----------
    request : Request
        The HTTP request object.
    
    Returns
    -------
    JSONResponse
        JSON response containing status and message.
    """
    try:
        _log("Accessing endpoint: /")
        return JSONResponse(
            content={"status": 200, "message": "Successful"},
            status_code=200,
        )    
    except Exception as e:
        _log(f"Internal Server Error: /candidate/{id}/recommendJobs", format="error")
        _log(str(e), format="error")
        _log(traceback.format_exc(), format="error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )