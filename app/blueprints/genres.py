from flask import Blueprint, render_template, request, redirect, url_for
from ..db_connect import get_db

genres = Blueprint('genres', __name__)


@genres.route('/')
def list_genres():  # Renamed function to avoid conflict
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM genres")  # Example table
        genres = cursor.fetchall()
    return render_template('genres.html', genres=genres)


@genres.route('/add', methods=['POST'])
def add_genre():
    name = request.form['name']

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO genres (name) VALUES (%s)", (name,))
        db.commit()
    return redirect(url_for('genres.genres'))


@genres.route('/delete/<int:id>')
def delete_genre(id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM genres WHERE id = %s", (id,))
        db.commit()
    return redirect(url_for('genres.genres'))
