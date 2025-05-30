from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus # Added for URL encoding credentials

# --- Database Configuration from Environment Variables ---
# The application expects the following environment variables to be set for DB connection:
# - DB_SERVER:  Hostname or IP address of the SQL Server instance. (Required)
# - DB_NAME:    The name of the database. (Required)
# - DB_USER:    Username for database authentication. (Required)
# - DB_PASSWORD: Password for database authentication. (Required)
# - DB_PORT:    Port number for the SQL Server instance. (Optional, defaults to "1433")
# - DB_DRIVER:  The ODBC driver string. (Optional, defaults to "ODBC Driver 18 for SQL Server")
#               Ensure the specified driver is installed in the environment.

raw_db_server = os.getenv("DB_SERVER")
raw_db_name = os.getenv("DB_NAME")
raw_db_user = os.getenv("DB_USER")
raw_db_password = os.getenv("DB_PASSWORD")

# Check for required environment variables
required_env_vars = {
    "DB_SERVER": raw_db_server,
    "DB_NAME": raw_db_name,
    "DB_USER": raw_db_user,
    "DB_PASSWORD": raw_db_password,
}

missing_vars = [key for key, value in required_env_vars.items() if value is None]
if missing_vars:
    raise ValueError(f"Missing required environment variables for database connection: {', '.join(missing_vars)}")

# URL-encode username and password
encoded_db_user = quote_plus(raw_db_user)
encoded_db_password = quote_plus(raw_db_password)

# Optional environment variables with defaults
db_port = os.getenv("DB_PORT", "1433")
# Spaces in the driver string must be replaced with '+' for the connection URL
db_driver_string = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server").replace(' ', '+')


# Construct the SQLAlchemy Database URL using encoded credentials
SQLALCHEMY_DATABASE_URL = \
    f"mssql+pyodbc://{encoded_db_user}:{encoded_db_password}@{raw_db_server}:{db_port}/{raw_db_name}?driver={db_driver_string}"

# --- SQLAlchemy Engine and Session Setup ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Example connection pool settings (SQLAlchemy defaults are often sufficient)
    # pool_size=5,
    # max_overflow=10,
    # pool_timeout=30, # seconds
    # pool_recycle=1800 # seconds (e.g., 30 minutes)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models should import Base from this file.
# e.g., from .database import Base
# The actual creation of tables (Base.metadata.create_all(bind=engine))
# is handled in main.py upon application startup.
