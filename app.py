from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import EditForm, AddForm
from models import db, Movie
import requests
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
TMDB_GENRE_LIST_URL = "https://api.themoviedb.org/3/genre/movie/list"

GENRE_MAP = {}

def load_genres():
    global GENRE_MAP
    response = requests.get(TMDB_GENRE_LIST_URL, params={"api_key": TMDB_API_KEY})
    if response.ok:
        genres = response.json().get("genres", [])
        GENRE_MAP = {genre["id"]: genre["name"] for genre in genres}
    else:
        print("⚠️ TMDb genre fetch failed.")
load_genres()

@app.route("/")
def home():
    search_query = request.args.get("q")
    genre_filter = request.args.get("genre")

    movies = Movie.query.order_by(Movie.rating.desc()).all()

    if search_query:
        movies = [m for m in movies if search_query.lower() in m.title.lower()]
    if genre_filter and genre_filter != "All":
        movies = [m for m in movies if genre_filter in m.genres.split(", ")]

    genres = sorted(set(genre for m in Movie.query.all() for genre in m.genres.split(", ") if genre))
    return render_template("index.html", movies=movies, genres=genres, selected_genre=genre_filter, search_query=search_query)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    session.pop('_flashes', None)  # Clear lingering messages
    if form.validate_on_submit():
        title = form.title.data
        try:
            response = requests.get(TMDB_SEARCH_URL, params={"api_key": TMDB_API_KEY, "query": title})
            response.raise_for_status()
            data = response.json().get("results")
            if not data:
                flash("No results found. Try another title.", "warning")
                return redirect(url_for("add"))
            return render_template("select.html", results=data)
        except requests.RequestException:
            flash("Failed to connect to TMDb.", "danger")
            return redirect(url_for("add"))
    return render_template("add.html", form=form)

@app.route("/select/<int:movie_id>")
def select(movie_id):
    try:
        details = requests.get(f"{TMDB_DETAILS_URL}{movie_id}", params={"api_key": TMDB_API_KEY}).json()
        genre_names = ", ".join([GENRE_MAP.get(g["id"], "Unknown") for g in details.get("genres", [])])
        new_movie = Movie(
            title=details.get("title", "Untitled"),
            year=details.get("release_date", "").split("-")[0] if details.get("release_date") else "N/A",
            description=details.get("overview", "No description available."),
            rating=0.0,
            review="",
            img_url=f"https://image.tmdb.org/t/p/w500{details['poster_path']}" if details.get("poster_path") else "",
            genres=genre_names
        )
        db.session.add(new_movie)
        db.session.commit()
        flash("✅ Movie added! Now rate and review it.", "success")
        return redirect(url_for("edit", movie_id=new_movie.id))
    except requests.RequestException:
        flash("Could not fetch movie details.", "danger")
        return redirect(url_for("add"))

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = EditForm(obj=movie)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        flash("✅ Movie updated successfully.", "success")
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie)

@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("❌ Movie deleted.", "danger")
    return redirect(url_for("home"))

@app.route("/stats")
def stats():
    genre_counts = db.session.query(Movie.genres).all()
    flat_genres = [g.strip() for row in genre_counts for g in row[0].split(", ") if g]
    genre_counter = Counter(flat_genres)
    return render_template("stats.html", genre_counts=genre_counter.items())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
