from flask import Blueprint, render_template, request, session, jsonify
import requests
import os

main_routes = Blueprint('main', __name__)
book_routes = Blueprint('books', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/get_started')
def get_started():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&key={api_key}'
    response = requests.get(url)
    books = response.json()
    
    genres = set()
    authors = set()
    for item in books.get('items', []):
        volume_info = item.get('volumeInfo', {})
        categories = volume_info.get('categories', [])
        for category in categories:
            genres.add(category)
        book_authors = volume_info.get('authors', [])
        for author in book_authors:
            authors.add(author)
    
    return render_template('get_started.html', genres=sorted(genres), authors=sorted(authors), books=books.get('items', []))

@main_routes.route('/get_books')
def get_books():
    author = request.args.get('author')
    genre = request.args.get('genre')
    language = request.args.get('langRestrict')
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    query = f'inauthor:{author}+subject:{genre}'
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict={language}&key={api_key}'
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