from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os # For potentially reading connection details from environment variables

# IMPORTANT: Replace placeholders with actual connection details or use environment variables.
# Example using environment variables (recommended for production):
# DB_USER = os.getenv("DB_USER", "your_user")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
# DB_SERVER = os.getenv("DB_SERVER", "your_server_name_or_ip")
# DB_PORT = os.getenv("DB_PORT", "1433") # Default MS SQL Server port
# DB_NAME = os.getenv("DB_NAME", "your_database_name")
# ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC+Driver+17+for+SQL+Server") # Ensure this driver is installed

# SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}?driver={ODBC_DRIVER}"

# Placeholder connection string - REPLACE THIS
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://<USER>:<PASSWORD>@<SERVER_NAME_OR_IP>:<PORT>/<DATABASE_NAME>?driver=ODBC+Driver+17+for+SQL+Server"
# Example for a local SQL Express instance with Windows Authentication:
# SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://localhost\\SQLEXPRESS/MyMetricsDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # pool_size=5, # Default is 5
    # max_overflow=10, # Default is 10
    # pool_timeout=30, # Default is 30 seconds
    # pool_recycle=1800 # Recycle connections after 30 minutes (optional)
    # connect_args are generally not needed for pyodbc unless for specific ODBC settings.
    # For pyodbc, connection string parameters are usually preferred.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Note: The create_tables function is not strictly necessary here if
# models.Base.metadata.create_all(bind=engine) is called directly in main.py,
# which is the current setup.
# def create_tables():
#     Base.metadata.create_all(bind=engine)

# Models should import Base from this file.
# e.g. from .database import Base
