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
COPY tests /app/tests
RUN pip install --no-cache-dir -r /app/search_recommend_api/requirements.txt
RUN pip install --no-cache-dir pytest coverage pytest-cov

CMD ["pytest", "--cov", "/app/tests/"]