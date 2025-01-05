import os
import http.server
import socketserver

# Set up the handler to serve files from the current directory
PORT = int(os.getenv("PORT", 8000))  # Use Replit's PORT environment variable
Handler = http.server.SimpleHTTPRequestHandler

# Start the server
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
