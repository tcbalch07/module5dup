from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret-key'  # Replace with a secure environment variable

# Register Blueprints for genres and movies
from app.blueprints.movies import movies
from app.blueprints.genres import genres
app.register_blueprint(movies)
app.register_blueprint(genres)

# Register direct routes
from app.routes import index, top_10
app.add_url_rule('/', view_func=index)
app.add_url_rule('/top10', view_func=top_10)

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)

