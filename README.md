# Top 10 Movies Web App

This is the web version of my original [Top 10 Movies CLI project](https://github.com/Cyber-Security-Tech/top-10-movies). It has been rebuilt as a full-stack Flask web application with database support, external API integration, and interactive features.

---

## Features

- Add movies by searching the TMDb API
- Select from live search results and auto-fill movie details
- Rate and review each movie
- Edit and delete entries from the list
- Filter movies by genre or search by keyword
- Display movie ratings as stars (out of 5)
- Clickable genre tags to instantly filter the homepage
- Genre statistics displayed using a pie chart (Chart.js)
- Flash messages and form validation with feedback

---

## Tech Stack

| Area        | Tools Used                                      |
|-------------|--------------------------------------------------|
| Backend     | Python, Flask, Flask-WTF, Flask-SQLAlchemy      |
| Frontend    | HTML, CSS, Bootstrap 5, Chart.js                |
| Database    | SQLite (via SQLAlchemy ORM)                     |
| API         | TMDb API (for movie data and genre information) |

---

## What I Learned

- Full-stack application architecture with Flask and Jinja2
- Structuring web apps with reusable components and templates
- Implementing search, filtering, and CRUD operations
- Validating form input with Flask-WTF and displaying helpful messages
- Using Chart.js to visualize statistics on the frontend
- Organizing static assets and templates for a scalable Flask project

---

## Future Improvements

- Deploy the web app using Render
- Cache genre list with automatic refresh to reduce API usage
- Add AI-powered movie recommendations based on user preferences
- Display embedded trailers using the YouTube API or TMDb video links

---

## Original CLI Version

This project is based on my earlier terminal-based version:  
🔗 [Top 10 Movies CLI Project](https://github.com/Cyber-Security-Tech/top-10-movies)

---

## Author

Created by [Cyber-Security-Tech](https://github.com/Cyber-Security-Tech)