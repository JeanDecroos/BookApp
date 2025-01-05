# filepath: /c:/Users/decroosb/Downloads/BookApp/main.py
from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import main_routes, book_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Use the secret key from .env file

# Register blueprints
app.register_blueprint(main_routes)
app.register_blueprint(book_routes)

if __name__ == '__main__':
    app.run(debug=True)