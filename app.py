# app.py
import os
import logging
from flask import Flask, jsonify
from datetime import datetime

# --- Configuration ---
# Use environment variables for configuration. This is a best practice for Docker
# and CI/CD pipelines, allowing different settings for different environments (dev, staging, prod).
# Default values provided for local development convenience.
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG_MODE = FLASK_ENV == 'development'
SECRET_KEY = os.environ.get('SECRET_KEY', 'a_super_secret_key_for_dev_only') # IMPORTANT: Change this for production!
APP_VERSION = os.environ.get('APP_VERSION', '0.0.1-dev') # Set by CI/CD pipeline, e.g., git SHA

# --- Logging Setup ---
# Configure logging for production. Flask's default debug logging is not suitable.
# Log to stdout/stderr so Docker can pick it up, and a logging agent can forward it.
logging.basicConfig(level=logging.INFO if not DEBUG_MODE else logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
    ENV=FLASK_ENV,
    DEBUG=DEBUG_MODE,
    # Add other configurations as needed, e.g., database URI, external service URLs
)

# --- Routes ---

@app.route('/')
def hello_world():
    """
    Root endpoint: Basic greeting.
    """
    app.logger.info("Accessing the root endpoint.")
    return 'Hello, Flask in Docker! This is version: {}'.format(APP_VERSION)

@app.route('/health')
def health_check():
    """
    Comprehensive health check endpoint.
    - Returns 200 OK if the application is fundamentally able to respond to requests.
    - Can be extended to check database connections, external services, etc.
    """
    app.logger.debug("Received health check request.")
    health_status = {
        "status": "UP",
        "timestamp": datetime.now().isoformat(),
        "application_version": APP_VERSION,
        "environment": FLASK_ENV,
        "checks": []
    }

    # --- Example of advanced health checks (uncomment and implement as needed) ---

    # 1. Database Connectivity Check (Example: using a dummy function)
    # def check_database_connection():
    #     try:
    #         # Replace with actual database connection test (e.g., ping, simple query)
    #         # import psycopg2
    #         # conn = psycopg2.connect(app.config['DATABASE_URI'])
    #         # conn.close()
    #         return True, "Database connection successful"
    #     except Exception as e:
    #         app.logger.error(f"Database check failed: {e}")
    #         return False, f"Database connection failed: {str(e)}"

    # db_ok, db_message = check_database_connection()
    # health_status["checks"].append({"name": "database", "status": "OK" if db_ok else "DOWN", "message": db_message})
    # if not db_ok:
    #     health_status["status"] = "DEGRADED" # Or "DOWN" based on criticality


    # 2. External Service Check (Example: using a dummy function)
    # def check_external_api():
    #     try:
    #         # Replace with actual HTTP request to an external API
    #         # import requests
    #         # response = requests.get(app.config['EXTERNAL_API_URL'], timeout=2)
    #         # response.raise_for_status()
    #         return True, "External API reachable"
    #     except Exception as e:
    #         app.logger.error(f"External API check failed: {e}")
    #         return False, f"External API unreachable: {str(e)}"

    # api_ok, api_message = check_external_api()
    # health_status["checks"].append({"name": "external_api", "status": "OK" if api_ok else "DOWN", "message": api_message})
    # if not api_ok and health_status["status"] == "UP": # Don't override if already DOWN from DB
    #     health_status["status"] = "DEGRADED"

    # --- End of example advanced checks ---

    status_code = 200
    if health_status["status"] == "DOWN":
        status_code = 503 # Service Unavailable
    elif health_status["status"] == "DEGRADED":
        status_code = 200 # Still OK, but with warnings (for monitoring systems)

    app.logger.debug(f"Health check response: {health_status['status']} with status code {status_code}")
    return jsonify(health_status), status_code

# Standard /status endpoint, often used for very basic liveness checks
@app.route('/status')
def status():
    """
    Simple status endpoint, primarily for liveness probes.
    Returns 200 OK if the Flask app process is running and able to serve requests.
    """
    app.logger.debug("Received status check request.")
    return 'OK', 200

# --- Production WSGI Server Execution ---
# This block is crucial for a production-grade Flask application.
# The built-in `app.run()` is only for development.
if __name__ == '__main__':
    # When running locally, directly execute the app for convenience.
    # In production, a WSGI server (like Gunicorn or uWSGI) will manage the app instance.
    if DEBUG_MODE:
        app.logger.info("Running Flask app in DEVELOPMENT mode. DO NOT USE IN PRODUCTION!")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # This block will likely not be executed directly in a Docker container
        # if you are using a proper WSGI server like Gunicorn as your ENTRYPOINT.
        # It's here as a fallback or for direct execution outside a WSGI server for testing.
        app.logger.info("Flask app configured for PRODUCTION. Please use a WSGI server (e.g., Gunicorn).")
        # Example of how you *would* run with Gunicorn if this was the entrypoint,
        # but typically Gunicorn is called directly from the Dockerfile's CMD/ENTRYPOINT.
        # from gunicorn.app.base import BaseApplication
        # class StandaloneApplication(BaseApplication):
        #     def __init__(self, app, options=None):
        #         self.application = app
        #         self.options = options or {}
        #         super().__init__()
        #     def load_config(self):
        #         for key, value in self.options.items():
        #             self.cfg.set(key.lower(), value)
        #     def load(self):
        #         return self.application
        # options = {
        #     'bind': '%s:%s' % ('0.0.0.0', 5000),
        #     'workers': os.environ.get('WEB_CONCURRENCY', 2), # Use WEB_CONCURRENCY from env
        #     'timeout': os.environ.get('GUNICORN_TIMEOUT', 30),
        #     'loglevel': 'info',
        #     'errorlog': '-', # Log to stderr
        #     'accesslog': '-', # Log to stdout
        # }
        # StandaloneApplication(app, options).run()
