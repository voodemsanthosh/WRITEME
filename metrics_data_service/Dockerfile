# Use python:3.9-alpine as a base image
FROM python:3.9-alpine

# Set environment variables for ODBC driver installation
ENV ACCEPT_EULA=Y \
    LANG=C.UTF-8

# Install system dependencies required for MS ODBC Driver on Alpine
# and other utilities.
RUN apk add --no-cache --virtual .build-deps unixodbc-dev build-base curl tar gnupg \
    && apk add --no-cache unixodbc libstdc++ su-exec \
    # Download and install msodbcsql17
    # Using Microsoft's official instructions for Alpine as a reference:
    # https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-linux%2Calpine17-linux%2Cdebian17-linux%2Credhat18-linux%2Credhat17-linux%2Csuse18-linux%2Csuse17-linux%2Cubuntu18-linux%2Cubuntu17-linux
    && curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17.tar.gz \
    && (gpg --keyserver hkps://keys.openpgp.org --recv-keys EB3E94ADBE1229CF \
        || gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys EB3E94ADBE1229CF) \
    && curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17.sig \
    && gpg --verify msodbcsql17.sig msodbcsql17.tar.gz \
    && tar -xzf msodbcsql17.tar.gz \
    && cd msodbcsql17-*/ \
    # The install.sh script might expect certain paths or utilities not common in minimal alpine
    # We might need to adjust or use its internal scripts like odbc_config directly if issues arise.
    # The --force option is used because the script might detect an "unsupported" distro.
    && ./install.sh install --accept-license --force \
    && cd .. \
    && rm -rf msodbcsql17.tar.gz msodbcsql17.sig msodbcsql17-* \
    # Clean up build dependencies
    && apk del .build-deps curl tar gnupg

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
