FROM python:3.9.16-slim-buster

# Set the working directory in the container
WORKDIR /app

# Set the environment variable for Elasticsearch URL given as an argument
ARG ES_URL
ENV ES_URL=${ES_URL}
ENV PYTHONPATH=/app


# Copy the project into the container at /app
COPY es_lib /app/es_lib
COPY search_recommend_api /app/search_recommend_api
RUN pip install --no-cache-dir -r /app/search_recommend_api/requirements.txt

EXPOSE 8080
CMD ["uvicorn", "search_recommend_api.main:app", "--host", "0.0.0.0", "--port", "8080"]