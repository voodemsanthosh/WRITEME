# Metrics Data Service

This service is a FastAPI application designed to collect, store, and retrieve metrics data.

## Project Structure

```
metrics_data_service/
├── app/                  # Core application logic
│   ├── __init__.py
│   ├── crud.py           # Database operations (Create, Read, Update, Delete)
│   ├── database.py       # Database setup and session management
│   ├── dependencies.py   # Dependency injection (e.g., DB session)
│   ├── models.py         # SQLAlchemy data models
│   ├── routers.py        # API route definitions
│   └── schemas.py        # Pydantic data validation schemas
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python package dependencies
└── README.md             # This file
# tests/                  # (To be added) Unit and integration tests
# .gitignore              # (To be added)
```

## Setup and Running

1.  **Navigate to the service directory:**
    ```bash
    cd metrics_data_service
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

5.  **Access API documentation:**
    Navigate to `http://127.0.0.1:8000/docs` in your browser to see the Swagger UI documentation.

## Database

The service is currently configured to use a SQLite database (`./metrics.db`), which will be created automatically when the application starts.
To use a different database (e.g., PostgreSQL), update the `SQLALCHEMY_DATABASE_URL` in `app/database.py` and install the appropriate database driver (e.g., `psycopg2-binary`).

## API Endpoints

All API endpoints are prefixed with `/api/v1`.

*   `POST /api/v1/metrics/`: Create a new metric.
*   `GET /api/v1/metrics/`: Retrieve a list of metrics.
*   `GET /api/v1/metrics/{metric_id}`: Retrieve a specific metric by its ID.

Refer to the `/docs` endpoint for detailed request and response schemas.

## Future Enhancements (TODO)

*   Add endpoints for updating and deleting metrics.
*   Implement authentication and authorization.
*   Add more robust error handling.
*   Implement database migrations (e.g., using Alembic).
*   Write comprehensive unit and integration tests.
*   Containerize the application using Docker.
*   Set up CI/CD pipelines.
