# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routes.resume_routes import router as resume_router
# Import route modules for different functionalities
from routes import auth_routes, user_routes, job_routes, application_routes, resume_routes

# Initialize the FastAPI application
app = FastAPI()

# Import the user_model (ensure it's correctly defined)
from models import user_model
# Import database configurations and Base for SQLAlchemy models
from database import Base, engine

# Create all tables defined in SQLAlchemy models if they don't exist
Base.metadata.create_all(bind=engine)

# Configure CORS middleware to allow cross-origin requests
# This is useful for development and testing, particularly with Swagger UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development - restrict in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include route handlers from different modules
# These routers define the API endpoints for authentication, users, jobs, and applications
app.include_router(auth_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router)
app.include_router(user_routes.router)
app.include_router(resume_routes.router)

# Custom OpenAPI schema generation with Bearer token security
# This function modifies the default OpenAPI schema to include JWT Bearer token authentication
def custom_openapi():
    # If the schema has already been generated, return it
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the default OpenAPI schema using FastAPI's built-in function
    openapi_schema = get_openapi(
        title="Job Application Tracking System",
        version="1.0.0",
        description="A backend API to track job applications and status.",
        routes=app.routes,
    )

    # Define the security scheme for Bearer token authentication
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Define the routes that require Bearer token authentication
    security_routes = ["/users/", "/jobs/", "/applications/"]  # Add routes that require security

    # Apply the security scheme to the specified routes
    for path, path_item in openapi_schema["paths"].items():
        if any(path.startswith(route) for route in security_routes):
            for method in path_item.values():
                method["security"] = [{"BearerAuth": []}]

    # Store the generated schema in the app instance
    app.openapi_schema = openapi_schema
    # Return the generated schema
    return app.openapi_schema

# Assign the custom_openapi function to app.openapi
# This ensures that the custom schema is used when generating the OpenAPI documentation
app.openapi = custom_openapi
