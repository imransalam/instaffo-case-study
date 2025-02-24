# Instaffo Case Study

## Problem statement
We are a recruitment agency and want to find the best candidates for jobs and best jobs for our candidates.
We are given an ElasticSearch instance with 2 indices, one for jobs and one for candidates.
We need to find the best candidates for the jobs and the best jobs for the candidates.
Furthermore we need to find the candidates and jobs based on their IDs as well

## Solution
We find this problem as a recommendation problem and we use three filters to solve this. These filters will help us find the best candidates for the jobs and the best jobs for the candidates.:
1. Salary match
2. Seniority match
3. Top skills match

## Data
The data is given by default as two JSON files, one for jobs and one for candidates. 
This data is then fed into an ElasticSearch instance as two seperate indices, one for jobs and one for candidates.

## Project Structure
We were given some modules of the code to start with. We had to add the business logic to the code as one module of the entire project. And this module is supposed to be a an API. We have chosed FastAPI as our framework for the API.

The project is divided into the following files and folders:
1. `documentation/` - This folder contains the documentation for the project. Specifically the readme file you are reading right now :)
2. `seed_image/` - This folder contains the data (candidates and jobs) that is fed into the ElasticSearch instance. The `configs` for elasticsearch are also present in this folder.
    1. `populate_es_indices.py` - A python script that reads the JSON of candidates and jobs and feeds it into the ElasticSearch instance.
    2. `es_configs/` - This folder contains the configurations for the ElasticSearch instance.
    3. `Dockerfile` - A dockerfile to create a docker image that runs the seeding script and then exits.
3. `es_lib/` - This folder contains the code that interacts with the ElasticSearch instance.
    1. `elastic_search_client.py` - This file contains the code that interacts with the ElasticSearch instance. It has several functions that let's the user build queries, aggregate queries and run the queries on the ElasticSearch instance.
    2. `exceptions.py` - This file contains the custom exceptions that are raised by the `elastic_search_client.py` file. Right now we only have one exception `IDNotFoundError`
4. `search_recommend_api/` - This folder contains the code for the API that is used to search and recommend jobs.
    1. `main.py` - A file that contains the main app of the FastAPI that imports different routers. And runs the API.
    2. `logger.py` - A logger file that let's us log the requests and responses of the API.
    3. `config.py` - A file that contains the configurations for the API.
    4. `Dockerfile` - A dockerfile to create a docker image that runs the API.
    5. `requirements.txt` - A file that contains the requirements for the API.
    6. `model/` - This folder contains the code for the models that are used in the API. This could also be called a `schema` folder.
        1. `job.py` - A file that contains the Job model that is used in the API.
        2. `candidate.py` - A file that contains the Candidate model that is used in the API.
        3. `filters.py` - A file that contains the filters model used when recommending jobs.
        4. `recommendation_response.py` - A file that contains the response model for the recommendation API.
    7. `routers/` - This folder contains the code for the routers that are used in the API.
        1. `candidates.py` - This file contains the code for the candidates router that is used in the API.
            * `GET candidate/{id}` - Endpoint to get a candidate by id.
            * `GET candidate/{id}/recommendJobs` - Endpoint to get recommended jobs for a candidate by id. This endpoint also takes three filters as query parameters: `salary_match`, `seniority_match`, and `top_skills_match`.
        2. `jobs.py` - This file contains the code for the jobs router that is used in the API.
            * `GET job/{id}` - Endpoint to get a job by id.
            * `GET job/{id}/recommendJobs` - Endpoint to get recommended candidates for a job by id. This endpoint also takes three filters as query parameters: `salary_match`, `seniority_match`, and `top_skills_match`.
        3. `index.py` - This file contains the code for the index router that is used in the API.
5. `tests/` - This folder contains the code for the tests that are used in the API.
    1. `test_main.py` - This file contains the code for the tests for the API
        * `test_api_health` - Test to check if the API is healthy. Pings the index and checks if 200 is returned
        * `test_candidates_endpoint` - Test to check if the get candidate endpoint is working. Checks if 200 is returned and if the candidate object is returned correctly
        * `test_recommend_jobs_endpoint` - Test to check if the get recommended jobs endpoint is working. Checks if 200 is returned and if the recommended jobs object is returned correctly
        * `test_jobs_endpoint` - Test to check if the get job endpoint is working. Checks if 200 is returned and if the job object is returned correctly
        * `test_recommend_candidates_endpoint` - Test to check if the get recommended candidates  endpoint is working. Checks if 200 is returned and if the recommended candidates object is returned correctly
    2. `Dockerfile` - This file contains the code for the Dockerfile that is used to build the test image.
6. `docker-compose.yml`
    * This builds the elasticsearch instance. 
    * This builds the Kibana instance for elasticsearch instance observability. 
    * This executes the Dockerfile that seeds the elasticsearch instance with the data from the `seed_image/data/` folder.
    * This executes the Dockerfile that builds the test image.
    * This executes the Dockerfile that builds the API image.