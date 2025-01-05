from flask import Flask, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def get_books():
    # Replace with your actual Google Books API key and query
    api_key = 'AIzaSyC5nqaKrpbREFeCdAAEjqOQtkckLUaUc5c'
    query = 'Roald Dahl'
    url = f'https://www.googleapis.com/books/v1/volumes?q=Roald%20Dahl&key={api_key}'
    response = requests.get(url)
    books = response.json()
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
