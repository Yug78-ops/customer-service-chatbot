from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "API is working!",
            "endpoints": [
                "/api/test",
                "/api/chat", 
                "/api/debug"
            ],
            "status": "success"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))