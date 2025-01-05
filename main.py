from flask import Flask, jsonify, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def get_books():
    api_key = 'AIzaSyC5nqaKrpbREFeCdAAEjqOQtkckLUaUc5c'
    author = request.args.get('author', 'Roald Dahl')
    url = f'https://www.googleapis.com/books/v1/volumes?q={author}&key={api_key}'
    response = requests.get(url)
    books = response.json()
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
