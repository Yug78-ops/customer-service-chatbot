from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import bleach
    BLEACH_AVAILABLE = True
except ImportError:
    BLEACH_AVAILABLE = False

# Get Gemini API key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if GOOGLE_API_KEY and GENAI_AVAILABLE:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

def load_pdf_content():
    """Load company information - simplified for serverless"""
    # For now, return a placeholder. In production, you might want to load this differently
    return """
    We are a customer service company that provides excellent support and solutions to our clients.
    Our services include technical support, customer inquiries, and comprehensive assistance.
    """

def get_styled_response(text):
    if BLEACH_AVAILABLE:
        sanitized_text = bleach.clean(text, tags=['p', 'br', 'span'], attributes={'span': ['style', 'class']})
        styled_text = f"<span class='bot-response-text'>{sanitized_text}</span>"
        return styled_text
    else:
        return f"<span class='bot-response-text'>{text}</span>"

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_message = data.get('message', '')
            
            if not user_message:
                response = {"error": "No message provided"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            if not GOOGLE_API_KEY or not GENAI_AVAILABLE:
                response = {"error": "API not properly configured"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            # Load company info
            company_info = load_pdf_content()
            
            # Construct a prompt that includes the company information
            prompt = f"Company Information:\n{company_info}\n\nUser Question: {user_message}\n\nPlease answer the user's question based on the company information provided. If the question is not related to the company or its services, politely redirect the conversation back to company-related topics."

            response_obj = model.generate_content(prompt)
            
            if hasattr(response_obj, 'text'):
                gemini_response = response_obj.text
            else:
                gemini_response = "Sorry, I encountered an error generating a response."

            styled_response = get_styled_response(gemini_response)
            response = {"response": styled_response}
            
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            response = {"error": f"An error occurred: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
