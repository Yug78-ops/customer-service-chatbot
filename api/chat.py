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
                
                # Process specific questions with tailored responses
                question = user_message.lower().strip()
                
                if "managing partner" in question or "partner" in question or "manager" in question:
                    bot_response = "<span class='bot-response-text'>The Managing Partner of TP Adhikari and Associates is Mr. Tara Prasad Adhikari. He has over 25 years of experience in accounting and financial consulting.</span>"
                
                elif "vision" in question or "company vision" in question:
                    bot_response = "<span class='bot-response-text'>Our vision is to be the most trusted financial advisory firm, known for our integrity, expertise, and client-centered approach. We aim to empower businesses through insightful financial guidance.</span>"
                
                elif "service" in question or "services" in question or "service areas" in question or "key service" in question:
                    bot_response = "<span class='bot-response-text'>Our key service areas include:<br>• Tax Planning and Advisory<br>• Financial Reporting and Analysis<br>• Business Consulting<br>• Audit and Assurance<br>• Corporate Finance<br>• Wealth Management</span>"
                
                elif "value" in question or "core values" in question:
                    bot_response = "<span class='bot-response-text'>Our core values are:<br>• Integrity and Ethics<br>• Client Focus<br>• Excellence<br>• Innovation<br>• Teamwork<br>• Community Engagement</span>"
                
                elif "location" in question or "office" in question or "where" in question or "address" in question:
                    bot_response = "<span class='bot-response-text'>Our office is located at: 123 Financial District, Kathmandu, Nepal. We are open Monday-Friday, 9:00 AM to 5:00 PM.</span>"
                    
                elif "contact" in question or "phone" in question or "email" in question or "reach" in question:
                    bot_response = "<span class='bot-response-text'>You can contact us through:<br>• Phone: +977 1234567890<br>• Email: info@tpadhikari.com<br>• Website: www.tpadhikari.com</span>"
                
                elif "hello" in question or "hi" in question or "hey" in question or "greetings" in question:
                    bot_response = "<span class='bot-response-text'>Hello! Welcome to TP Adhikari and Associates. How can I assist you today?</span>"
                
                else:
                    bot_response = f"<span class='bot-response-text'>You asked about '{user_message}'. Currently, I have limited information on this topic. For detailed assistance, please contact our team at info@tpadhikari.com or call +977 1234567890.</span>"
            else:
                bot_response = "<span class='bot-response-text'>Hello! I am TP Adhikari and Associates Customer Services chatbot. How can I help you today?</span>"
                
            response = {
                "response": bot_response
            }
        except Exception as e:
            response = {
                "error": str(e)
            }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
