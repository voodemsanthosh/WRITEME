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

## Database Configuration

The service is configured to connect to a Microsoft SQL Server database. Connection details must be provided via environment variables. The application will not start if the required variables are missing.

### Environment Variables

The following environment variables are used to configure the database connection:

*   `DB_SERVER`: **(Required)** The hostname or IP address of your MS SQL Server instance.
*   `DB_NAME`: **(Required)** The name of the database to connect to.
*   `DB_USER`: **(Required)** The username for database authentication.
*   `DB_PASSWORD`: **(Required)** The password for database authentication.
*   `DB_PORT`: (Optional) The port number for the MS SQL Server instance. Defaults to `1433` if not set.
*   `DB_DRIVER`: (Optional) The ODBC driver string that pyodbc should use. Defaults to `"ODBC Driver 18 for SQL Server"` if not set. Ensure the specified driver is installed in the environment where the application runs (e.g., within the Docker container).

For example, when running locally or with Docker:
```bash
export DB_SERVER="your_sql_server_host"
export DB_NAME="your_database_name"
export DB_USER="your_username"
export DB_PASSWORD="your_secret_password"
# export DB_PORT="1433" # Optional
# export DB_DRIVER="ODBC Driver 18 for SQL Server" # Optional
uvicorn main:app --reload
```

The `Dockerfile` provided with this service installs "ODBC Driver 18 for SQL Server". If you use a different driver, ensure it's correctly installed and update the `DB_DRIVER` environment variable accordingly.

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
