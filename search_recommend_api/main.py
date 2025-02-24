"""
This script is the entry point for running a FastAPI server to handle API requests.

Key Components:
- FastAPI Application: Initializes the FastAPI app with necessary middleware and routes.
- CORS Middleware: Configures Cross-Origin Resource Sharing (CORS) to allow requests from any origin.
- API Routing: Includes a router from the `api.controller` module to manage endpoint handlers.

Environment Configurations:
- PORT: The server's port can be defined via the `APP_PORT` environment variable or defaults from `ApiConfig`.
- HOST: The server's host can be set by the `APP_HOST` environment variable or through `ApiConfig`.

Usage:
Execute this script to start the FastAPI application with predefined configurations.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the router for process handling
from search_recommend_api.router.index import router as index_router
from search_recommend_api.router.candidates import router as candidates_router
from search_recommend_api.router.jobs import router as jobs_router

# Import configuration class for API settings
from search_recommend_api.config import ApiConfig

# Initialize the FastAPI app
app: FastAPI = FastAPI()

# Load configuration settings
cnf: ApiConfig = ApiConfig()

# Set the port and host using environment variables or fallback to config defaults
selected_port: int = int(os.environ.get("APP_PORT", cnf.PORT))
selected_host: str = str(os.environ.get("APP_HOST", cnf.HOST))

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Include router for process handling
app.include_router(index_router)
app.include_router(candidates_router)
app.include_router(jobs_router)

if __name__ == "__main__":
    # Output to indicate where the server is starting
    print(f"Starting FastAPI server on port {selected_port}")
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host=selected_host, port=selected_port, reload=False)