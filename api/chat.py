from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # Response for GET requests (for browser testing)
        response = {
            "message": "Chat API is working",
            "status": "success",
            "usage": "Send a POST request to this endpoint to chat with the bot"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # Always return a simple hardcoded response
        response = {
            "response": "<span class='bot-response-text'>Hello! I'm working now. This is a test response from TP Adhikari and Associates. How can I help you today?</span>"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
