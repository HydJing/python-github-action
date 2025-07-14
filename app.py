# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask in Docker!'

@app.route('/status')
def status():
    return 'OK'

if __name__ == '__main__':
    # This ensures the app runs on all available network interfaces
    # and in debug mode for development.
    app.run(debug=True, host='0.0.0.0')
