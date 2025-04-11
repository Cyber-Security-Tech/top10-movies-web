from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.String(10))
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    review = db.Column(db.Text)
    img_url = db.Column(db.String(500))
    genres = db.Column(db.String(250))  
