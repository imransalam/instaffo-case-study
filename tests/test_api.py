import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from search_recommend_api.main import app  
from search_recommend_api.model.candidate import Candidate
from search_recommend_api.model.job import Job
from search_recommend_api.model.recommendation_response import RecommendationResponse

client = TestClient(app)

def test_api_health():
    response = client.get("/")
    assert response.status_code == 200

def test_candidates_endpoint():
    response = client.get("/candidate/1")
    assert response.status_code == 200
    
    # Check if the response JSON can be parsed into a Candidate model
    candidate_data = response.json()
    try:
        candidate = Candidate(**candidate_data)
        assert candidate is not None
    except ValidationError as e:
        pytest.fail(f"Candidate data validation failed: {e}")

def test_jobs_endpoint():
    response = client.get("/job/1")
    assert response.status_code == 200
    
    # Check if the response JSON can be parsed into a Job model
    job_data = response.json()
    try:
        job = Job(**job_data)
        assert job is not None
    except ValidationError as e:
        pytest.fail(f"Job data validation failed: {e}")

def test_recommend_candidates_endpoint():
    response = client.get("/job/1/recommendCandidates?top_skills_match=true&seniority_match=true&salary_match=true")
    assert response.status_code == 200
    
    # Check if the response JSON can be parsed into a Job model
    output_data = response.json()
    try:
        assert isinstance(output_data, list)
        output = RecommendationResponse(**output_data[0])
        assert output is not None
    except ValidationError as e:
        pytest.fail(f"Output data validation failed: {e}")

def test_recommend_jobs_endpoint():
    response = client.get("/candidate/1/recommendJobs?top_skills_match=true&seniority_match=true&salary_match=true")
    assert response.status_code == 200
    
    # Check if the response JSON can be parsed into a Job model
    output_data = response.json()
    try:
        assert isinstance(output_data, list)
        output = RecommendationResponse(**output_data[0])
        assert output is not None
    except ValidationError as e:
        pytest.fail(f"Output data validation failed: {e}")