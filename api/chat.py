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
        
        # Get the content length to read the request body
        content_length = int(self.headers.get('Content-Length', 0))
        
        try:
            # Read the request body if it exists
            if content_length > 0:
                request_body = self.rfile.read(content_length).decode('utf-8')
                request_data = json.loads(request_body)
                user_message = request_data.get('message', '')
                
                # Log the message we received (helpful for debugging)
                print(f"Received message: {user_message}")
                
                # Generate a response based on the user message
                bot_response = f"<span class='bot-response-text'>You asked: '{user_message}'. This is a test response from TP Adhikari and Associates. How can I help you further?</span>"
            else:
                bot_response = "<span class='bot-response-text'>Hello! I'm working now. This is a test response from TP Adhikari and Associates. How can I help you today?</span>"
                
            response = {
                "response": bot_response
            }
        except Exception as e:
            response = {
                "error": str(e)
            }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
