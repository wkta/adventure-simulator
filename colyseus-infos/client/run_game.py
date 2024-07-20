import http.server
import socketserver
import os
import webbrowser
import threading
import time


def open_url_in_new_tab(url):
    webbrowser.open_new_tab(url)


def open_website_after_delay(delay_s, given_url):
    def wrapper():
        time.sleep(delay_s)
        open_url_in_new_tab(given_url)
    
    thread = threading.Thread(target=wrapper)
    thread.start()


# Define the port
PORT = 8000

# Define the directory to serve files from
# WEB_DIR = os.path.join(os.path.dirname(__file__), 'client')
WEB_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    url_to_open = f"http://localhost:{PORT}"
    open_website_after_delay(1.77, url_to_open)
    
    os.chdir(WEB_DIR)
    # Create a simple HTTP request handler
    Handler = http.server.SimpleHTTPRequestHandler
    # Create a TCP server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()
