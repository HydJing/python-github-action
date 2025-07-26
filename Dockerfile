# Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
# This step is done early to leverage Docker's build cache.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .

# Install Python dependencies, including Gunicorn for production
# --no-cache-dir ensures that pip does not store downloaded packages, reducing image size
# --upgrade pip ensures pip is up-to-date
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Declare a build-time argument for the application version.
# This will be passed from your GitHub Actions workflow (e.g., --build-arg APP_VERSION=${{ github.sha }}).
ARG APP_VERSION=unknown

# Set environment variables for the Flask application.
# FLASK_ENV is set to production by default inside the container.
ENV FLASK_ENV=production
# APP_VERSION is set from the build argument.
ENV APP_VERSION=${APP_VERSION}
# Define default number of Gunicorn workers. Can be overridden at runtime.
# A common heuristic is (2 * CPU_CORES) + 1. Adjust based on your server's CPU.
ENV GUNICORN_WORKERS=4
# Set Gunicorn timeout (in seconds)
ENV GUNICORN_TIMEOUT=30
# Set Gunicorn log level
ENV GUNICORN_LOGLEVEL=info


# Copy the rest of the application code into the container
# This should be done after installing dependencies to again leverage caching.
COPY . .

# Expose port 5000, which is where Gunicorn will listen
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn.
# 'app:app' refers to the 'app' Flask instance within your 'app.py' file.
# The --bind 0.0.0.0:5000 makes Gunicorn listen on all network interfaces on port 5000.
# --workers uses the GUNICORN_WORKERS environment variable.
# --timeout uses the GUNICORN_TIMEOUT environment variable.
# --log-level uses the GUNICORN_LOGLEVEL environment variable.
# --access-logfile and --error-logfile '-' direct logs to stdout/stderr for Docker.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "${GUNICORN_WORKERS}", \
     "--timeout", "${GUNICORN_TIMEOUT}", \
     "--log-level", "${GUNICORN_LOGLEVEL}", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]
