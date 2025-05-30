from contextlib import asynccontextmanager
from typing import AsyncGenerator # For Python < 3.9, else not needed for this
from fastapi import FastAPI

# Assuming 'engine' and 'models' are imported from .src.database and .src.models
from .src import models
from .src.database import engine
from .src.routers import metrics_router # Keep existing router import

# Lifespan context manager
@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]: # Renamed app to app_instance to avoid conflict
    # This code runs on startup
    print("INFO:     Running application startup via lifespan event...")
    # Check if engine is a MagicMock (indicating a test environment with mocking)
    # The check for 'mock_calls' is a common way to identify a unittest.mock.MagicMock instance.
    # hasattr(engine, 'mock_calls') might be too generic if other objects use that attribute.
    # A more specific check could be isinstance(engine, MagicMock) if MagicMock is imported here,
    # or by checking a custom attribute set on the mock engine in tests.
    # For now, assuming 'mock_calls' is a reasonable heuristic for this project's tests.
    if hasattr(engine, 'mock_calls') or type(engine).__name__ == 'MagicMock':
        print("INFO:     Mock engine detected, skipping models.Base.metadata.create_all during lifespan startup.")
    else:
        print("INFO:     Real engine detected, calling models.Base.metadata.create_all during lifespan startup.")
        # In a production scenario, you might want migrations (e.g., Alembic) instead of create_all.
        models.Base.metadata.create_all(bind=engine)
    yield
    # This code runs on shutdown (if needed)
    print("INFO:     Running application shutdown via lifespan event...")

# Initialize FastAPI app with the lifespan manager
app = FastAPI(
    title="Metrics Data Service",
    description="A FastAPI service to collect and retrieve metrics data.",
    version="0.1.0",
    lifespan=lifespan # Pass the lifespan manager
)

# Include the API router (ensure this is after app is defined)
app.include_router(metrics_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Metrics Data Service. Navigate to /docs for API documentation."}

# TODO: Add exception handlers
# TODO: Add middleware (e.g., for logging, authentication)

if __name__ == "__main__":
    import uvicorn
    # Note: Uvicorn should ideally be run as a separate process in production (e.g., using Gunicorn)
    # The "main:app" string refers to this file (main.py) and the 'app' FastAPI instance.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
