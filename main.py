import json
import webbrowser
import os

# Step 1: Configuration
TITLE = "The World of Roald Dahl"
AUTHOR = "Roald Dahl"

# Step 2: Generate HTML (Simulating book data for now)
def generate_html(books):
    print("Generating HTML file...")
    html_content = "<html><head><title>Book Data</title></head><body>"
    for book in books:
        html_content += f"<h2>{book['title']}</h2>"
        html_content += f"<p>Author: {book['author']}</p>"
        html_content += f"<p>Page Count: {book['pageCount']}</p>"
        html_content += f"<p>ISBN: {book['isbn']}</p>"
        html_content += "<hr>"
    html_content += "</body></html>"

    with open("index.html", "w") as f:
        f.write(html_content)
    print("HTML file saved as 'index.html'.")

# Simulating books data (for testing without requests)
books = [
    {
        "title": "The World of Roald Dahl",
        "author": "Roald Dahl",
        "pageCount": 288,
        "isbn": "9780141365508"
    },
    {
        "title": "James and the Giant Peach",
        "author": "Roald Dahl",
        "pageCount": 192,
        "isbn": "9780142410350"
    }
]

# Step 3: Main Execution
if __name__ == "__main__":
    # Generate the HTML file
    if books:
        generate_html(books)

        # Check if the HTML file exists before trying to open it
        if os.path.exists("index.html"):
            print("Opening the HTML file in your browser...")
            try:
                # Open the HTML file in the browser using its absolute path
                full_path = os.path.abspath("index.html")
                webbrowser.open_new_tab(f"file://{full_path}")
            except Exception as e:
                print(f"Could not open browser: {e}")
        else:
            print("index.html not found.")
    else:
        print("No books found to display.")
