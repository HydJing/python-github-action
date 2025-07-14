# Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir ensures that pip does not store downloaded packages, reducing image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000, which is the default Flask port
EXPOSE 5000

# Define the command to run the Flask application when the container starts
CMD ["python", "app.py"]
