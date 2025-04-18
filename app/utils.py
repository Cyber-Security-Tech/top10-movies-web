"""
utils.py — Utility functions and TMDb integration for the Top 10 Movies web app.

Handles genre mapping, movie searching, detailed movie info retrieval via TMDb API,
and direct YouTube trailer link resolution via the YouTube Data API.
"""

import os
import requests

# Global dictionary to store TMDb genre ID to name mapping
GENRE_MAP = {}

def load_genres():
    """
    Fetch and cache the list of TMDb movie genres.

    Populates the global GENRE_MAP dictionary, which maps genre ID to genre name.
    """
    global GENRE_MAP
    TMDB_GENRE_LIST_URL = "https://api.themoviedb.org/3/genre/movie/list"
    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        print("❌ TMDb API key not found. Check your .env file.")
        return

    try:
        response = requests.get(TMDB_GENRE_LIST_URL, params={"api_key": api_key})
        response.raise_for_status()
        genres = response.json().get("genres", [])
        GENRE_MAP = {genre["id"]: genre["name"] for genre in genres}
    except requests.RequestException as e:
        print(f"⚠️ TMDb genre fetch failed: {e}")


def search_movies_by_title(title):
    """
    Search TMDb for movies by title.

    Returns:
        - List of result dictionaries if found
        - Empty list if no results
        - None if request fails
    """
    TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        print("❌ TMDb API key not found.")
        return None

    try:
        response = requests.get(TMDB_SEARCH_URL, params={"api_key": api_key, "query": title})
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"⚠️ Search request failed: {e}")
        return None


def get_movie_details(movie_id):
    """
    Get full details for a movie by its TMDb ID.

    Returns:
        - A dict with all required fields for DB insert
        - None if request fails
    """
    TMDB_DETAILS_URL = f"https://api.themoviedb.org/3/movie/{movie_id}"
    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        print("❌ TMDb API key not found.")
        return None

    try:
        response = requests.get(TMDB_DETAILS_URL, params={"api_key": api_key})
        response.raise_for_status()
        data = response.json()

        title = data.get("title", "Untitled")
        year = data.get("release_date", "").split("-")[0] if data.get("release_date") else "N/A"
        description = data.get("overview", "No description available.")
        img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else ""
        genres = ", ".join([GENRE_MAP.get(g["id"], "Unknown") for g in data.get("genres", [])])

        return {
            "title": title,
            "year": year,
            "description": description,
            "img_url": img_url,
            "genres": genres
        }

    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch movie details: {e}")
        return None


def get_youtube_trailer_url(title):
    """
    Use the YouTube Data API to find a trailer video for the given movie title.

    Returns:
        - Direct YouTube video URL if found
        - None if no trailer is found or request fails
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

    if not api_key:
        print("❌ YouTube API key not found.")
        return None

    params = {
        "part": "snippet",
        "q": f"{title} trailer",
        "key": api_key,
        "maxResults": 1,
        "type": "video"
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
    except requests.RequestException as e:
        print(f"⚠️ YouTube API request failed: {e}")

    return None
