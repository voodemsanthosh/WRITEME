from fastapi import FastAPI
from .src.routers import metrics_router  # Import the specific router
from .src.database import engine
from .src import models

# Create database tables on startup
# This will create tables based on models that use the Base from database.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Metrics Data Service",
    description="A FastAPI service to collect and retrieve metrics data.",
    version="0.1.0"
)

# Include the API router
app.include_router(metrics_router, prefix="/api/v1") # Use the imported metrics_router

@app.get("/")
async def root():
    return {"message": "Welcome to the Metrics Data Service. Navigate to /docs for API documentation."}

# TODO: Add exception handlers
# TODO: Add middleware (e.g., for logging, authentication)

if __name__ == "__main__":
    import uvicorn
    # Note: Uvicorn should ideally be run as a separate process in production (e.g., using Gunicorn)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # Added reload=True for dev
