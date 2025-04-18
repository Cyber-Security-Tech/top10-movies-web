import os
from flask import Flask
from dotenv import load_dotenv
from .models import db

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret")

    # Initialize database
    db.init_app(app)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    
    with app.app_context():
        db.create_all()

    return app
