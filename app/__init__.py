"""
__init__.py — Application factory and app configuration for the Top 10 Movies web app.

Initializes Flask extensions, loads environment variables, and registers blueprints.
"""

import os
from flask import Flask
from dotenv import load_dotenv
from .models import db  # ✅ Import from models.py

# Load environment variables from .env file
load_dotenv()


def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    # Basic configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/movies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Create database tables (only during development)
    with app.app_context():
        if app.debug:
            db.create_all()

    return app
