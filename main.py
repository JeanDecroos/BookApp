from flask import Flask, jsonify, render_template, request, session
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_started')
def get_started():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&key={api_key}'
    response = requests.get(url)
    books = response.json()
    
    genres = set()
    for item in books.get('items', []):
        volume_info = item.get('volumeInfo', {})
        categories = volume_info.get('categories', [])
        for category in categories:
            genres.add(category)
    
    return render_template('get_started.html', genres=sorted(genres))

@app.route('/books')
def get_books():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    author = request.args.get('author', 'Roald Dahl')
    genre = request.args.get('genre', '')
    language = request.args.get('langRestrict', 'en')
    query = f'{author}+{genre}'
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict={language}&key={api_key}'
    print(f"Making API call to: {url}")  # Log the API call
    response = requests.get(url)
    books = response.json()
    return jsonify(books)

@app.route('/add_to_reading_list', methods=['POST'])
def add_to_reading_list():
    book = request.json
    if 'reading_list' not in session:
        session['reading_list'] = []
    session['reading_list'].append(book)
    session.modified = True  # Ensure the session is marked as modified
    return jsonify({'status': 'success'})

@app.route('/reading_list')
def reading_list():
    reading_list = session.get('reading_list', [])
    session.pop('reading_list', None)  # Clear the reading list from the session
    return render_template('reading_list.html', reading_list=reading_list)

@app.route('/progress')
def progress():
    return render_template('progress.html')

if __name__ == '__main__':
    app.run(debug=True)