from flask import Blueprint, render_template, request, redirect, url_for
from ..db_connect import get_db
from ..functions import filter_by_genre, filter_by_title, filter_by_year

movies = Blueprint('movies', __name__)


@movies.route('/movie')
def movie():
    db = get_db()

    # Fetch all genres for the dropdown
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM genres")
        genres = cursor.fetchall()

    # Fetch all movies with their genres
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT movies.id, movies.title, movies.year, GROUP_CONCAT(genres.name SEPARATOR ', ') AS genres
            FROM movies
            LEFT JOIN movie_genres ON movies.id = movie_genres.movie_id
            LEFT JOIN genres ON movie_genres.genre_id = genres.id
            GROUP BY movies.id
        """)
        movies = cursor.fetchall()  # Fetch all movies with grouped genres

    return render_template('movies.html', movies=movies, genres=genres)


@movies.route('/filter', methods=['GET'])
def filter():
    title = request.args.get('title')
    genre_id = request.args.get('genre')
    year = request.args.get('year')

    if title:
        movies = filter_by_title(title)
    elif genre_id:
        movies = filter_by_genre(genre_id)
    elif year:
        movies = filter_by_year(year)
    else:
        movies = []  # Empty list if no filter is applied

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM genres")
        genres = cursor.fetchall()

    return render_template('movies.html', movies=movies, genres=genres)


@movies.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        genre_ids = request.form.getlist('genre_ids')  # Multiple genres

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO movies (title, year) VALUES (%s, %s)", (title, year))
            movie_id = cursor.lastrowid
            for genre_id in genre_ids:
                cursor.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))
            db.commit()
        return redirect(url_for('movies.movies'))

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM genres")
        genres = cursor.fetchall()
    return render_template('add_movie.html', genres=genres)


@movies.route('/delete/<int:id>')
def delete_movie(id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM movie_genres WHERE movie_id = %s", (id,))
        cursor.execute("DELETE FROM movies WHERE id = %s", (id,))
        db.commit()
    return redirect(url_for('movies.movies'))


@movies.route('/update/<int:id>', methods=['GET', 'POST'])
def update_movie(id):
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        genre_ids = request.form.getlist('genre_ids')

        with db.cursor() as cursor:
            cursor.execute("UPDATE movies SET title = %s, year = %s WHERE id = %s", (title, year, id))
            cursor.execute("DELETE FROM movie_genres WHERE movie_id = %s", (id,))
            for genre_id in genre_ids:
                cursor.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (id, genre_id))
            db.commit()
        return redirect(url_for('movies.movies'))

    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM movies WHERE id = %s", (id,))
        movie = cursor.fetchone()

        cursor.execute("SELECT * FROM genres")
        genres = cursor.fetchall()

        cursor.execute("SELECT genre_id FROM movie_genres WHERE movie_id = %s", (id,))
        selected_genres = [row['genre_id'] for row in cursor.fetchall()]

    return render_template('update_movie.html', movie=movie, genres=genres, selected_genres=selected_genres)

