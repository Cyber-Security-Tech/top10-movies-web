"""
run.py — Entry point for the Flask application.

This file initializes and runs the Flask server using the application
factory pattern defined in app/__init__.py.

Compatible with both local development and Render deployment.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
