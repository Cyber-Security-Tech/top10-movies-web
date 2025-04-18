"""
models.py — SQLAlchemy database models for the Top 10 Movies web app.

Defines the Movie table schema.
"""

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance, initialized in app/__init__.py
db = SQLAlchemy()


class Movie(db.Model):
    """
    Movie model representing a single movie entry in the database.
    Includes metadata, user rating/review, TMDb poster/genre data, and YouTube trailer link.
    """
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.String(10), nullable=True)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    review = db.Column(db.Text, nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.String(250), nullable=True)
    trailer_url = db.Column(db.String(300), nullable=True)  

    def __repr__(self):
        return f"<Movie {self.title} ({self.year}) - Rating: {self.rating}>"
