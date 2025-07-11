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
            
            try:
                # Check if model is properly initialized
                if model is None:
                    response = {"error": "Gemini model initialization failed. Please check your API key and try again."}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    return
                
                # Simple prompt to test API functionality
                prompt = f"""You are a helpful customer service chatbot for an audit and financial advisory firm.
                
                Question: {user_message}
                
                Please respond briefly and professionally."""
                
                print(f"Sending prompt to Gemini API, length: {len(prompt)} characters")
                
                # Generate response with safety parameters
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                ]
                
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 200,
                }
                
                # Generate response using the API with safety settings
                response_obj = model.generate_content(
                    prompt, 
                    safety_settings=safety_settings,
                    generation_config=generation_config
                )
                
                print("API response received")
                
                if hasattr(response_obj, 'text'):
                    gemini_response = response_obj.text
                    print(f"Response text length: {len(gemini_response)} characters")
                else:
                    print("No text attribute in response")
                    print(f"Response object: {str(response_obj)}")
                    gemini_response = "Thank you for your question. As a customer service representative, I'd be happy to help with your inquiry about our services."
                
                styled_response = get_styled_response(gemini_response)
                response = {"response": styled_response}
                
            except Exception as api_error:
                print(f"API Error: {str(api_error)}")
                # Provide a fallback response instead of an error
                fallback_response = "Thank you for your question. I'm currently experiencing some technical difficulties. Please try again in a moment or contact our support team for immediate assistance."
                styled_fallback = get_styled_response(fallback_response)
                response = {"response": styled_fallback}
            
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
