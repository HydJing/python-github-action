# Flask Dockerized Application

This repository contains a simple Flask web application, containerized with Docker, and integrated with GitHub Actions for continuous integration, including building, unit testing, and security scanning.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Local Development Setup](#local-development-setup)
    * [Running with Python](#running-with-python)
    * [Running with Docker](#running-with-docker)
* [Testing](#testing)
* [CI/CD Pipeline (GitHub Actions)](#cicd-pipeline-github-actions)
* [File Structure](#file-structure)
* [Contributing](#contributing)
* [License](#license)

---

## Project Overview

This project demonstrates a basic Flask application, `app.py`, designed to be run within a Docker container. It includes:
* A simple "Hello, World!" endpoint (`/`).
* A status endpoint (`/status`).
* A `Dockerfile` for building a lightweight Docker image.
* `requirements.txt` to manage Python dependencies.
* Unit tests (`test_app.py`) using `pytest`.
* A GitHub Actions workflow (`.github/workflows/flask-ci.yml`) to automate:
    * Building the Docker image.
    * Running unit tests.
    * Performing a static security analysis using Bandit.

---

## Features

* **Simple Flask App**: A minimal Flask application for demonstration.
* **Dockerized**: Easily build and run the application in an isolated Docker container.
* **Unit Testing**: Automated tests to ensure application functionality.
* **Security Scanning**: Static code analysis with Bandit to identify potential security vulnerabilities.
* **GitHub Actions CI/CD**: Automated workflow for builds, tests, and scans on every push and pull request to the `main` branch.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* [Git](https://git-scm.com/downloads)
* [Python 3.9+](https://www.python.org/downloads/) (for local development without Docker)
* [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
* [Docker](https://docs.docker.com/get-docker/) (for containerized development and running)

---

## Local Development Setup

### Running with Python

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-github-repo.git](https://github.com/your-username/your-github-repo.git)
    cd your-github-repo
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

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000` or `http://localhost:5000`.

### Running with Docker

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-github-repo.git](https://github.com/your-username/your-github-repo.git)
    cd your-github-repo
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t flask-app-image .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 flask-app-image
    ```
    The application will be accessible at `http://127.0.0.1:5000` or `http://localhost:5000`.

---

## Testing

Unit tests are written using `pytest`.

1.  **Ensure dependencies are installed (if running locally without Docker):**
    ```bash
    pip install -r requirements.txt pytest
    ```

2.  **Run tests:**
    ```bash
    pytest
    ```

---

## CI/CD Pipeline (GitHub Actions)

This project uses GitHub Actions to automate the continuous integration process. The workflow is defined in `.github/workflows/flask-ci.yml`.

The workflow triggers on `push` and `pull_request` events to the `main` branch and performs the following jobs:

* **`build-and-test`**:
    * Checks out the code.
    * Sets up Python.
    * Installs Python dependencies.
    * Runs unit tests using `pytest`.
    * Builds the Docker image.
* **`security-scan`**:
    * Checks out the code.
    * Sets up Python.
    * Installs Bandit.
    * Runs a static security analysis using Bandit on the Python code.
    * Uploads the Bandit report as an artifact.
    * *(Optional: If uncommented in the workflow, it also runs Trivy for Docker image vulnerability scanning and uploads its report.)*

You can view the status of your workflows and detailed logs in the "Actions" tab of your GitHub repository.

---

## File Structure