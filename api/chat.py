from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse
import sys

# Print Python version for debugging
print(f"Python version: {sys.version}")

# Import Google Generative AI
try:
    import google.generativeai as genai
    print("Successfully imported google.generativeai")
    GENAI_AVAILABLE = True
except ImportError as e:
    print(f"Failed to import google.generativeai: {e}")
    GENAI_AVAILABLE = False

# We don't need PyPDF2 for serverless, so we'll skip it
PYPDF2_AVAILABLE = False

# Import bleach for HTML sanitization
try:
    import bleach
    print("Successfully imported bleach")
    BLEACH_AVAILABLE = True
except ImportError as e:
    print(f"Failed to import bleach: {e}")
    BLEACH_AVAILABLE = False

# Get Gemini API key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Strip quotes if they exist (sometimes environment variables have quotes)
if GOOGLE_API_KEY and (GOOGLE_API_KEY.startswith('"') and GOOGLE_API_KEY.endswith('"')) or (GOOGLE_API_KEY.startswith("'") and GOOGLE_API_KEY.endswith("'")):
    GOOGLE_API_KEY = GOOGLE_API_KEY[1:-1]

# Initialize the model if we have the API key and the library
if GOOGLE_API_KEY and GENAI_AVAILABLE:
    try:
        print(f"Configuring Gemini API with key: {GOOGLE_API_KEY[:5]}...{GOOGLE_API_KEY[-4:]} (key truncated for security)")
        genai.configure(api_key=GOOGLE_API_KEY)
        # Use gemini-1.0-pro instead as it's more widely available and stable
        model = genai.GenerativeModel('gemini-1.0-pro')
        print("Successfully configured the Gemini model")
    except Exception as config_error:
        print(f"Error configuring Gemini: {config_error}")
        model = None
else:
    print(f"API Key available: {bool(GOOGLE_API_KEY)}, GENAI_AVAILABLE: {GENAI_AVAILABLE}")
    model = None

def load_pdf_content():
    """Load company information - simplified for serverless"""
    # In serverless environment, we can't rely on loading local files the same way
    # So we use a placeholder text that contains our company information
    return """
    Our company offers comprehensive audit and advisory services to businesses of all sizes.
    We specialize in financial audits, tax advisory, risk management, and business consulting.
    Our team of certified professionals ensures compliance with all regulatory requirements.
    We provide personalized solutions tailored to each client's unique needs and challenges.
    Our services include annual financial statement audits, internal control assessments,
    tax planning and compliance, due diligence for mergers and acquisitions, and strategic business advice.
    We pride ourselves on maintaining the highest standards of integrity, confidentiality, and professional excellence.
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

            if not GOOGLE_API_KEY:
                response = {"error": "API key not found in environment variables"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
                
            if not GENAI_AVAILABLE:
                response = {"error": "Google Generative AI module not available"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            # Load company info
            company_info = load_pdf_content()
            
            # Bypass all API calls and use hardcoded responses for now
            print("Using hardcoded response system")
            
            # Map of predefined responses based on keywords in the user's question
            responses = {
                "office": "Our main office is located at 123 Business Avenue, Suite 500, in the Financial District. We are open Monday through Friday from 9:00 AM to 5:30 PM.",
                "location": "Our main office is located at 123 Business Avenue, Suite 500, in the Financial District.",
                "services": "We offer a comprehensive range of services including financial audits, tax advisory, risk management, business consulting, and strategic planning tailored to your needs.",
                "audit": "Our audit services include financial statement audits, compliance audits, internal audits, and specialized industry audits performed by our team of certified professionals.",
                "tax": "Our tax services include tax planning, compliance, advisory for both individuals and businesses, and specialized support for international taxation matters.",
                "contact": "You can contact us via email at info@tpadhikari.com, by phone at (555) 123-4567, or by visiting our office during business hours.",
                "hours": "Our office is open Monday through Friday from 9:00 AM to 5:30 PM. We are closed on weekends and major holidays.",
                "team": "Our team consists of certified accountants, financial analysts, tax specialists, and industry experts with extensive experience in various business sectors.",
                "cost": "Our service fees vary based on the scope and complexity of your needs. We offer free initial consultations to discuss your requirements and provide a detailed quote.",
                "consulting": "Our consulting services help businesses optimize operations, improve financial performance, manage risk, and achieve strategic objectives."
            }
            
            # Default response if no keywords match
            default_response = "Thank you for your question. As a representative of TP Adhikari and Associates, I'd be happy to provide information about our audit and advisory services. Could you please provide more details about what specific information you're looking for?"
            
            # Check for keywords in the user's message
            user_message_lower = user_message.lower()
            selected_response = default_response
            
            for keyword, response_text in responses.items():
                if keyword in user_message_lower:
                    selected_response = response_text
                    break
            
            # Apply styling to the response
            styled_response = get_styled_response(selected_response)
            response = {"response": styled_response}
            
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Server Error: {str(e)}")
            # Always return a user-friendly response rather than exposing the error
            fallback_response = "Thank you for your message. Our system is currently experiencing some technical difficulties. Please try again later or contact our support team for assistance."
            styled_fallback = f"<span class='bot-response-text'>{fallback_response}</span>"
            response = {"response": styled_fallback}
            try:
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except:
                # Last resort if even the error handling fails
                simple_response = {"response": "System error. Please try again."}
                self.wfile.write(json.dumps(simple_response).encode('utf-8'))
