from .db_connect import get_db

def filter_by_genre(genre_id):
    """Retrieve all movies associated with a specific genre ID."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT movies.id, movies.title, movies.year, GROUP_CONCAT(genres.name SEPARATOR ', ') AS genres
            FROM movies
            JOIN movie_genres ON movies.id = movie_genres.movie_id
            JOIN genres ON movie_genres.genre_id = genres.id
            WHERE genres.id = %s
            GROUP BY movies.id
        """, (genre_id,))
        movies = cursor.fetchall()
    return movies

def filter_by_title(title):
    """Retrieve movies where the title matches or contains the search term."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT movies.id, movies.title, movies.year, GROUP_CONCAT(genres.name SEPARATOR ', ') AS genres
            FROM movies
            LEFT JOIN movie_genres ON movies.id = movie_genres.movie_id
            LEFT JOIN genres ON movie_genres.genre_id = genres.id
            WHERE movies.title LIKE %s
            GROUP BY movies.id
        """, ('%' + title + '%',))
        movies = cursor.fetchall()
    return movies

def filter_by_year(year):
    """Retrieve all movies released in a specific year."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT movies.id, movies.title, movies.year, GROUP_CONCAT(genres.name SEPARATOR ', ') AS genres
            FROM movies
            LEFT JOIN movie_genres ON movies.id = movie_genres.movie_id
            LEFT JOIN genres ON movie_genres.genre_id = genres.id
            WHERE movies.year = %s
            GROUP BY movies.id
        """, (year,))
        movies = cursor.fetchall()
    return movies

