# Flask Dockerized Application

This repository contains a robust Flask web application, containerized with Docker, and integrated with GitHub Actions for continuous integration and continuous delivery (CI/CD). This setup includes extensive testing, multiple layers of security scanning, artifact management, automated deployments to staging and production environments, and notifications.

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

This project demonstrates a production-ready Flask application, `app.py`, designed for deployment within Docker containers. It now includes advanced features and a mature CI/CD pipeline:

* **Enhanced Flask Application (`app.py`)**: Features an extended health check endpoint, robust logging, and configuration via environment variables suitable for various environments (development, staging, production).
* **Production-Ready Dockerfile**: Utilizes `gunicorn` as the WSGI server for efficient and stable production deployment, building lightweight Docker images.
* **Split Dependencies**: `requirements.txt` for production runtime dependencies and `requirements-dev.txt` for development/testing tools.
* **Comprehensive Testing (`test_app.py`)**: Unit tests using `pytest`, including detailed assertions for the new health endpoint.
* **Advanced GitHub Actions CI/CD (`.github/workflows/flask-ci.yml`)**: An extensive automated workflow that covers:
    * Code quality and style checks (linting).
    * Multiple layers of security scanning (SAST, dependency vulnerability, secret detection, Docker image vulnerability).
    * Thorough unit and mutation testing.
    * Automated Docker image building and pushing to GitHub Container Registry (GHCR).
    * Software Bill of Materials (SBOM) generation for enhanced supply chain security.
    * Automated deployments to staging and production environments (with manual approval for production via GitHub Environments).
    * Post-deployment smoke tests on staging.
    * Automated notifications for pipeline success and failure.
    * Automated release notes generation.

---

## Features

* **Robust Flask App**: Minimal yet production-ready Flask application with configurable environments and comprehensive health checks.
* **Containerized (Docker)**: Optimized `Dockerfile` for building secure, lightweight, and performant Docker images using Gunicorn.
* **Layered Testing**:
    * **Unit Testing**: Automated tests with `pytest` and `pytest-cov` for code coverage.
    * **Mutation Testing**: Assesses the effectiveness and quality of your test suite.
* **Multi-Stage Security Scanning**:
    * **Static Application Security Testing (SAST)**: Bandit for Python code analysis.
    * **Dependency Vulnerability Scan**: `pip-audit` to check for known vulnerabilities in Python packages.
    * **Secrets Scanning**: `gitleaks` to prevent accidental credential leakage in the codebase.
    * **Container Image Security Scan**: Trivy for deep vulnerability scanning of Docker images.
* **Software Bill of Materials (SBOM)**: Automatically generates an SBOM using `syft`, enhancing software supply chain visibility.
* **GitHub Actions CI/CD**: Fully automated pipeline with:
    * Code quality and formatting checks (`flake8`, `black`).
    * Automated Docker image build and push to GHCR.
    * **Automated Deployments**: To staging and production environments, leveraging GitHub Environments for protection and visibility.
    * **Post-Deployment Verification**: Automated smoke tests on staging after deployment.
    * **Notifications**: Slack notifications for pipeline success (production) and failures.
    * **Automated Release Notes**: Generates release notes based on merged pull requests.

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

3.  **Install development and application dependencies:**
    ```bash
    pip install -r requirements-dev.txt
    ```

4.  **Run the Flask application in development mode:**
    ```bash
    FLASK_ENV=development python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000` or `http://localhost:5000`.

### Running with Docker

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-github-repo.git](https://github.com/your-username/your-github-repo.git)
    cd your-github-repo
    ```

2.  **Build the Docker image:**
    This command will build the production-ready image, including Gunicorn.
    ```bash
    docker build -t flask-app-image:latest .
    ```

3.  **Run the Docker container:**
    This will run the application using Gunicorn, exposing port 5000.
    ```bash
    docker run -p 5000:5000 -e FLASK_ENV=development flask-app-image:latest
    ```
    The application will be accessible at `http://127.0.0.1:5000` or `http://localhost:5000`.

---

## Testing

Unit and mutation tests are integrated into the CI/CD pipeline, but you can also run them locally.

1.  **Ensure development dependencies are installed:**
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Run all tests (unit tests and coverage):**
    ```bash
    pytest --cov=. --cov-report=term-missing
    ```

3.  **Run mutation tests:**
    ```bash
    mutmut run --paths-to-mutate "app/" --tests-dir "tests/"
    ```
    *(Adjust paths if your application or test files are in different directories.)*

---

## CI/CD Pipeline (GitHub Actions)

This project leverages a sophisticated GitHub Actions workflow defined in `.github/workflows/flask-ci.yml`. It automates the entire CI/CD process from code commit to production deployment.

The workflow triggers on `push` and `pull_request` events to the `main` branch, and also allows manual `workflow_dispatch` for specific deployments.

Here's a breakdown of the jobs:

* **`lint`**: Performs code style and quality checks using `flake8` and `black`.
* **`source-code-security-scan`**: Conducts Static Application Security Testing (SAST) on the Python codebase using `Bandit`.
* **`dependency-scan`**: Scans Python dependencies for known vulnerabilities using `pip-audit`.
* **`secrets-scan`**: Detects accidentally committed secrets using `gitleaks`.
* **`unit-tests`**: Runs comprehensive unit tests with `pytest` and generates a code coverage report.
* **`mutation-tests`**: Executes mutation tests using `mutmut` to assess the quality and effectiveness of the existing test suite.
* **`build-and-push-docker-image`**: Builds the production Docker image and pushes it to GitHub Container Registry (GHCR), tagged with the commit SHA and `latest` (on `main` branch pushes).
* **`docker-image-security-scan`**: Performs a vulnerability scan on the built Docker image using `Trivy`.
* **`generate-sbom`**: Creates a Software Bill of Materials (SBOM) for the Docker image using `Syft`, enhancing software supply chain visibility.
* **`deploy-to-staging`**: Deploys the application to the staging environment. This job depends on all prior CI and security checks passing. It integrates with GitHub Environments.
* **`staging-smoke-test`**: After a successful staging deployment, runs quick automated smoke tests against the deployed application to ensure basic functionality.
* **`deploy-to-production`**: Deploys the application to the production environment. This job is configured with GitHub Environment protection rules, typically requiring manual approval, and only proceeds after a successful staging deployment and smoke test.
* **`create-release-notes`**: Automatically generates and drafts release notes on GitHub after a successful production deployment to the `main` branch.
* **`notify-on-failure`**: Sends a Slack notification if any job in the pipeline fails.
* **`notify-on-success`**: Sends a Slack notification upon a successful production deployment.

You can view the status of your workflows and detailed logs in the "Actions" tab of your GitHub repository.

---

## File Structure
