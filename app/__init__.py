from flask import Flask
from .routes import main_routes, book_routes
from config import Config
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'))
    app.config.from_object(Config)
    app.register_blueprint(main_routes, url_prefix='/')
    app.register_blueprint(book_routes, url_prefix='/books')
    return app