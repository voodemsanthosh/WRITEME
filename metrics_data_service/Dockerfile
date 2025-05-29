# Use python:3.9-alpine as a base image
FROM python:3.9-alpine

# Set environment variables for ODBC driver installation
ENV ACCEPT_EULA=Y \
    LANG=C.UTF-8

# --- Application Environment Variables ---
# Database connection details.
# These are placeholders and should be overridden at runtime with actual deployment values.
# Refer to README.md for more details on these variables.
ENV DB_SERVER="your_sql_server_host"
ENV DB_NAME="your_database_name"
ENV DB_USER="your_db_user"
ENV DB_PASSWORD="" # IMPORTANT: This is sensitive and MUST be overridden at runtime. Do not commit default passwords.
ENV DB_PORT="1433"
ENV DB_DRIVER="ODBC Driver 18 for SQL Server" # Ensure this driver is installed in the image.

# Install system dependencies required for MS ODBC Driver 18 on Alpine
RUN apk add --no-cache --virtual .build-deps curl gnupg \
    && apk add --no-cache unixodbc libstdc++ \
    # Download and install msodbcsql18 using .apk package
    # Following Microsoft's official instructions for Alpine (ODBC Driver 18):
    # https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-linux
    && ODBC_DRIVER_VERSION="18.5.1.1-1" \
    && ARCHITECTURE="amd64" \
    && ODBC_DRIVER_PACKAGE="msodbcsql18_${ODBC_DRIVER_VERSION}_${ARCHITECTURE}.apk" \
    && ODBC_DRIVER_SIGNATURE="msodbcsql18_${ODBC_DRIVER_VERSION}_${ARCHITECTURE}.sig" \
    && ODBC_DRIVER_URL_BASE="https://download.microsoft.com/download/fae28b9a-d880-42fd-9b98-d779f0fdd77f" \
    && curl -O "${ODBC_DRIVER_URL_BASE}/${ODBC_DRIVER_PACKAGE}" \
    && curl -O "${ODBC_DRIVER_URL_BASE}/${ODBC_DRIVER_SIGNATURE}" \
    # Import Microsoft GPG key
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import - \
    # Verify signature
    && gpg --verify "${ODBC_DRIVER_SIGNATURE}" "${ODBC_DRIVER_PACKAGE}" \
    # Install the package
    # The .apk package should handle its own dependencies like unixodbc if correctly built by Microsoft.
    # We keep unixodbc in 'apk add' for explicitness and in case of partial .apk dependencies.
    && apk add --allow-untrusted "./${ODBC_DRIVER_PACKAGE}" \
    # Clean up downloaded files and build dependencies
    && rm -f "./${ODBC_DRIVER_PACKAGE}" "./${ODBC_DRIVER_SIGNATURE}" \
    && apk del .build-deps curl gnupg

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# This assumes the Dockerfile is in metrics_data_service/
# and src/ contains the application modules, main.py is at the same level as src/
COPY ./src /app/src
COPY ./main.py /app/main.py
# COPY ./README.md /app/README.md # README is optional, can be excluded

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
# 'app' is the FastAPI instance variable in 'main.py' (at /app/main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
