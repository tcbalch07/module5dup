from flask import Flask
from .db_connect import get_db, close_db
from .blueprints.movies import movies_bp
from .blueprints.genres import genres_bp
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(movies_bp, url_prefix='/movies')
    app.register_blueprint(genres_bp, url_prefix='/genres')

    # Ensure the database connection is closed after each request
    app.teardown_appcontext(close_db)

    return app




