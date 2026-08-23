import http.server
import socketserver
import webbrowser
import os
import socket

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    global PORT
    for port in range(8000, 8010):
        try:
            httpd = ReusableTCPServer(("", port), Handler)
            PORT = port
            break
        except OSError:
            continue
            
    print(f"==================================================")
    print(f"  BIOSENTINEL-OS SOFTWARE PROTOTYPE SERVER")
    print(f"==================================================")
    print(f"Running locally at: http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop the server.")
    
    webbrowser.open(f"http://localhost:{PORT}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
