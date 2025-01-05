from flask import Blueprint, render_template, request, session, jsonify
import requests
import os

main_routes = Blueprint('main', __name__)
book_routes = Blueprint('books', __name__)

def fetch_authors():
    url = "https://www.googleapis.com/books/v1/volumes?q=*&maxResults=40"
    response = requests.get(url)
    data = response.json()
    
    authors = set()
    for item in data.get('items', []):
        volume_info = item.get('volumeInfo', {})
        authors_list = volume_info.get('authors', [])
        authors.update(authors_list)
    
    return list(authors)[:2]  # Limit to 2 authors

def fetch_genres():
    url = "https://www.googleapis.com/books/v1/volumes?q=*&maxResults=40"
    response = requests.get(url)
    data = response.json()
    
    genres = set()
    for item in data.get('items', []):
        volume_info = item.get('volumeInfo', {})
        categories = volume_info.get('categories', [])
        genres.update(categories)
    
    return list(genres)[:1]  # Limit to 1 genre

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/get_started')
def get_started():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    query = 'subject:fiction'
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=40'
    response = requests.get(url)
    books = response.json()
    
    all_books = books.get('items', [])
    all_authors = fetch_authors()
    all_genres = fetch_genres()
    
    return render_template('get_started.html', genres=sorted(all_genres), authors=sorted(all_authors), books=all_books)

@main_routes.route('/get_books')
def get_books():
    author = request.args.get('author')
    genre = request.args.get('genre')
    language = request.args.get('langRestrict')
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    
    query_parts = []
    if author and author != 'all':
        query_parts.append(f'inauthor:{author}')
    if genre and genre != 'all':
        query_parts.append(f'subject:{genre}')
    query = '+'.join(query_parts) if query_parts else '*'
    
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict={language if language != "all" else ""}&key={api_key}'
    response = requests.get(url)
    books = response.json()
    return jsonify(books)

@book_routes.route('/add_to_reading_list', methods=['POST'])
def add_to_reading_list():
    book = request.json
    reading_list = session.get('reading_list', [])
    
    # Check if the book is already in the reading list
    for item in reading_list:
        if item['id'] == book['id']:
            return jsonify({'status': 'error', 'message': 'Book already in reading list'})
    
    # Add the book to the reading list
    reading_list.append(book)
    session['reading_list'] = reading_list
    return jsonify({'status': 'success', 'message': 'Book added to reading list'})

@book_routes.route('/reading_list')
def reading_list():
    return render_template('reading_list.html')

@book_routes.route('/progress')
def progress():
    return render_template('progress.html')