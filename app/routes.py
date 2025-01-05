# filepath: /c:/Users/decroosb/Downloads/BookApp/routes.py
from flask import Blueprint, render_template, request, jsonify, session
import requests
import os

main_routes = Blueprint('main', __name__)
book_routes = Blueprint('books', __name__)

def fetch_authors():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes?q=*&maxResults=40&key={api_key}"
    response = requests.get(url)
    books = response.json()
    authors = set()
    for item in books.get('items', []):
        volume_info = item.get('volumeInfo', {})
        author_list = volume_info.get('authors', [])
        for author in author_list:
            authors.add(author)
    return authors

def fetch_genres():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes?q=*&maxResults=40&key={api_key}"
    response = requests.get(url)
    books = response.json()
    genres = set()
    for item in books.get('items', []):
        volume_info = item.get('volumeInfo', {})
        categories = volume_info.get('categories', [])
        for category in categories:
            genres.add(category)
    return genres

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/get_started')
def get_started():
    authors = fetch_authors()
    genres = fetch_genres()
    return render_template('get_started.html', authors=authors, genres=genres)

@main_routes.route('/get_books')
def get_books():
    author = request.args.get('author', 'all')
    genre = request.args.get('genre', 'all')
    lang_restrict = request.args.get('langRestrict', 'all')
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    query = "subject:fiction"
    if author != 'all':
        query += f"+inauthor:{author}"
    if genre != 'all':
        query += f"+subject:{genre}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict={lang_restrict}&key={api_key}"
    response = requests.get(url)
    books = response.json()
    return jsonify(books)

@book_routes.route('/add_to_reading_list', methods=['POST'])
def add_to_reading_list():
    book = request.json
    reading_list = session.get('reading_list', [])
    for item in reading_list:
        if item['id'] == book['id']:
            return jsonify({'status': 'error', 'message': 'Book already in reading list'})
    reading_list.append(book)
    session['reading_list'] = reading_list
    return jsonify({'status': 'success', 'message': 'Book added to reading list'})

@book_routes.route('/reading_list')
def reading_list():
    reading_list = session.get('reading_list', [])
    return render_template('reading_list.html', reading_list=reading_list)

@book_routes.route('/progress')
def progress():
    reading_list = session.get('reading_list', [])
    total_pages = sum(book.get('pageCount', 0) for book in reading_list)
    total_pages_read = sum(book.get('pagesRead', 0) for book in reading_list)
    overall_progress = (total_pages_read / total_pages) * 100 if total_pages > 0 else 0
    return render_template('progress.html', total_pages=total_pages, total_pages_read=total_pages_read, overall_progress=overall_progress)