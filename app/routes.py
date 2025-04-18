"""
routes.py — All route definitions and business logic for the Top 10 Movies web app.

Handles homepage rendering, movie search/add/edit/delete operations,
and genre-based statistics. Uses TMDb API for external movie data.
"""

import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .forms import EditForm, AddForm
from .models import db, Movie
from .utils import (
    load_genres,
    GENRE_MAP,
    search_movies_by_title,
    get_movie_details,
    get_youtube_trailer_url  # ✅ added here
)
from collections import Counter

main = Blueprint("main", __name__)

# Preload genre mapping from TMDb API
load_genres()


@main.route("/")
def home():
    """
    Homepage — shows top 10 movies with optional search and genre filtering.
    """
    search_query = request.args.get("q")
    genre_filter = request.args.get("genre")

    # Start with all movies sorted by rating
    query = Movie.query.order_by(Movie.rating.desc())

    if search_query:
        query = query.filter(Movie.title.ilike(f"%{search_query}%"))

    movies = query.all()

    if genre_filter and genre_filter != "All":
        movies = [m for m in movies if genre_filter in m.genres.split(", ")]

    genres = sorted(set(
        genre for m in Movie.query.all()
        for genre in m.genres.split(", ") if genre
    ))

    return render_template("index.html", movies=movies, genres=genres,
                           selected_genre=genre_filter, search_query=search_query)


@main.route("/add", methods=["GET", "POST"])
def add():
    """
    Step 1 — Search for a movie title using TMDb API.
    """
    form = AddForm()
    session.pop('_flashes', None)

    if form.validate_on_submit():
        title = form.title.data
        results = search_movies_by_title(title)

        if results is None:
            flash("Failed to connect to TMDb.", "danger")
            return redirect(url_for("main.add"))

        if not results:
            flash("No results found. Try another title.", "warning")
            return redirect(url_for("main.add"))

        return render_template("select.html", results=results)

    return render_template("add.html", form=form)


@main.route("/select/<int:movie_id>")
def select(movie_id):
    """
    Step 2 — After selecting from search results, fetch details and add movie.
    """
    details = get_movie_details(movie_id)
    if not details:
        flash("Could not fetch movie details.", "danger")
        return redirect(url_for("main.add"))

    # Prevent duplicates based on title and year
    existing = Movie.query.filter_by(
        title=details["title"],
        year=details["year"]
    ).first()

    if existing:
        flash("This movie already exists in your list.", "info")
        return redirect(url_for("main.home"))

    # ✅ Get YouTube trailer link
    trailer_url = get_youtube_trailer_url(details["title"])

    new_movie = Movie(
        title=details["title"],
        year=details["year"],
        description=details["description"],
        rating=0.0,
        review="",
        img_url=details["img_url"],
        genres=details["genres"],
        trailer_url=trailer_url  # ✅ Save trailer link
    )

    db.session.add(new_movie)
    db.session.commit()
    flash("✅ Movie added! Now rate and review it.", "success")
    return redirect(url_for("main.edit", movie_id=new_movie.id))


@main.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    """
    Edit rating and review for a movie.
    """
    movie = Movie.query.get_or_404(movie_id)
    form = EditForm(obj=movie)

    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        flash("✅ Movie updated successfully.", "success")
        return redirect(url_for("main.home"))

    return render_template("edit.html", form=form, movie=movie)


@main.route("/delete/<int:movie_id>")
def delete(movie_id):
    """
    Delete a movie from the database.
    """
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("❌ Movie deleted.", "danger")
    return redirect(url_for("main.home"))


@main.route("/stats")
def stats():
    """
    Display genre frequency analytics.
    """
    genre_counts = db.session.query(Movie.genres).all()
    flat_genres = [g.strip() for row in genre_counts for g in row[0].split(", ") if g]
    genre_counter = Counter(flat_genres)
    return render_template("stats.html", genre_counts=genre_counter.items())
