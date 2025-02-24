from dotenv import load_dotenv
import os
from typing import Union
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from es_lib.exceptions import IDNotFoundError
from search_recommend_api.model.filters import Filters
from search_recommend_api.model.recommendation_response import RecommendationResponse
load_dotenv(override=True)
ES_URL = os.getenv("ES_URL")


class ElasticsearchClient:
    """
    Class containing methods for retrieving jobs or candidates from the
    respective Elasticsearch index by ID as well as sending queries.

    Args:
        index (str): "candidates"
    """

    __client = Elasticsearch(ES_URL)

    def __init__(self, index) -> None:
        self.index = index

    def get_entity(
        self,
        *,
        id: int,
    ) -> dict:
        """
        Returns the document corresponding to the given document ID as dictionary.

        Args:
            id (int): ID of the document to return.

        Returns:
            dict: Entity object corresponding to the given ID.

        Raises:
            IDNotFoundError: If the ID was not found in the index.
        """

        try:
            return self.__client.get_source(index=self.index, id=id, _source=True)
        except NotFoundError as error:
            raise IDNotFoundError(
                "ID '{}' was not found in the index '{}'.".format(id, self.index)
            ) from error

    def get_recommendation_type_output(
        self,
        *,
        response
    ) -> list[RecommendationResponse]:
        """
        Utility function to post process the response from Elasticsearch.

        Args:
            response: The raw response from Elasticsearch.
        
        Returns:
            RecommendationResponse: The post processed response as a list of RecommendationResponse objects.
        """
        if not response:
            raise ValueError("Response is empty")
        if "hits" not in response:
            raise ValueError("Response does not contain hits")
        if "hits" not in response["hits"]:
            raise ValueError("Response does not contain hits")
        if not response["hits"]["hits"]:
            raise ValueError("Response does not contain hits")
        
        return [RecommendationResponse(
               id=hit["_id"],
               relevance_score=hit["_score"]
        ) for hit in response["hits"]["hits"]]

    def build_salary_match_query(
        self,
        *,
        salary_data: Union[int, float]
    ) -> dict:
        """
        Builds a query to match the salary of the entity.

        Args:
            salary_data: The salary data of the entity to be queried.
        
        Returns:
            The salary match query.
        """
        if not salary_data:
            raise ValueError("Salary data is empty")
        
        if self.index == "candidates":
            return {
                "range": {"salary_expectation": {"lte": salary_data}} # Get candidates where the salary expectation is less than or equal to the job's max salary
            }
        else:  # jobs
            return {
                "range": {"max_salary": {"gte": salary_data}} # Get jobs where the max salary is greater than or equal to the candidate's salary expectation
            }
    
    def build_seniority_match_query(
        self,
        *,
        seniority_data: Union[list[str], str]
    ) -> dict:
        """
        Builds a query to match the seniority of the entity.

        Args:
            seniority_data: The seniority data of the entity to be queried.
        
        Returns:
            The seniority match query.
        """
        if not seniority_data:
            raise ValueError("Seniority data is empty")
        
        if self.index == "candidates":
            return {
                "terms": {"seniority": seniority_data} # Get candidates where the seniority matches the job's seniority
            }
        else:  # jobs
            return {
                "terms": {"seniorities": [seniority_data]} # Get jobs where the seniority matches the candidate's seniority
            }
        
    def build_top_skills_match_query(
        self,
        *,
        top_skills_data: list[str]
    ) -> dict:
        """
        Builds a query to match the top skills of the entity.

        Args:
            top_skills_data: The top skills data of the entity to be queried.
        
        Returns:
            The top skills match query.
        """
        if not top_skills_data:
            raise ValueError("Top skills data is empty")
        
        return {
            "terms_set": {
                "top_skills": {
                    "terms": top_skills_data,
                    "minimum_should_match_script": {
                        "source": "Math.min(params.num_terms, 2)",
                        "params": {"num_terms": len(top_skills_data)}
                    }
                }
            }
        }
    def build_should_queries(
        self,
        *,
        entity_data: dict = None,
        filters_used: Filters = Filters()
    ) -> list[dict]:
        """
        Builds a list of should queries based on the user's data and provided filters.

        Args:
            entity_type: Either candidate or job, depending on which index is being queried.
            entity_data: The data of the entity to be queried.
        
        Returns:
            The should queries based on the user's data and provided filters.
        """
        if not (entity_data and filters_used):
            raise ValueError("Both entitiy_data and filters_used are empty")

        should_queries: list[dict] = []
        if filters_used.top_skills_match == True and "top_skills" in entity_data:
            should_queries.append(
                self.build_top_skills_match_query(
                    top_skills_data=entity_data["top_skills"]
                    )
                )
        if filters_used.seniority_match == True and ("seniority" in entity_data or "seniorities" in entity_data):
            should_queries.append(
                self.build_seniority_match_query(
                    seniority_data=entity_data["seniorities"] if self.index == "candidates" else entity_data["seniority"]
                )
            )
        if filters_used.salary_match == True and ("max_salary" in entity_data or "salary_expectation" in entity_data):
            should_queries.append(
                self.build_salary_match_query(
                    salary_data=entity_data["max_salary"] if self.index == "candidates" else entity_data["salary_expectation"]
                )
            )
        return should_queries
        
    def search_with_bool_queries(
        self,
        *,
        should_queries: list[dict] = None,
        must_queries: list[dict] = None,
        return_source=False,
    ):
        """
        Builds a boolean query comprising the provided should and must sub queries.

        Args:
            should_queries: the sub-queries that are to be concatenated by the OR operator
            must_queries: the sub-queries that are to be concatenated by the AND operator
            return_source: whether to return the _source field of the document.

        Returns:
            The matching documents.
        """
        if not (should_queries or must_queries):
            raise ValueError("Either should_queries or must_queries must be set.")

        query = {
            "query": {
                "bool": {"must": must_queries or [], "should": should_queries or []}
            }
        }
        return self.search(query=query, return_source=return_source)

    def search(self, query: dict, return_source=False) -> dict:
        """
        Executes a query on the index.
        """
        return self.__client.search(body=query, index=self.index, source=return_source)
