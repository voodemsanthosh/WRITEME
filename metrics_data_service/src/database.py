from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# --- Database Configuration from Environment Variables ---
# The application expects the following environment variables to be set for DB connection:
# - DB_SERVER:  Hostname or IP address of the SQL Server instance. (Required)
# - DB_NAME:    The name of the database. (Required)
# - DB_USER:    Username for database authentication. (Required)
# - DB_PASSWORD: Password for database authentication. (Required)
# - DB_PORT:    Port number for the SQL Server instance. (Optional, defaults to "1433")
# - DB_DRIVER:  The ODBC driver string. (Optional, defaults to "ODBC Driver 18 for SQL Server")
#               Ensure the specified driver is installed in the environment.

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Check for required environment variables
required_env_vars = {
    "DB_SERVER": DB_SERVER,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
}

missing_vars = [key for key, value in required_env_vars.items() if value is None]
if missing_vars:
    raise ValueError(f"Missing required environment variables for database connection: {', '.join(missing_vars)}")

# Optional environment variables with defaults
DB_PORT = os.getenv("DB_PORT", "1433")
# Spaces in the driver string must be replaced with '+' for the connection URL
DB_DRIVER_STRING = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server").replace(' ', '+')


# Construct the SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URL = \
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}?driver={DB_DRIVER_STRING}"

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
