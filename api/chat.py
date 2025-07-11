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

# Strip quotes if they exist (sometimes environment variables have quotes)
if GOOGLE_API_KEY and (GOOGLE_API_KEY.startswith('"') and GOOGLE_API_KEY.endswith('"')) or (GOOGLE_API_KEY.startswith("'") and GOOGLE_API_KEY.endswith("'")):
    GOOGLE_API_KEY = GOOGLE_API_KEY[1:-1]

# Initialize the model if we have the API key and the library
if GOOGLE_API_KEY and GENAI_AVAILABLE:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("Successfully configured the Gemini model")
    except Exception as config_error:
        print(f"Error configuring Gemini: {config_error}")
        model = None
else:
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
                # Construct a prompt that includes the company information
                prompt = f"""You are a customer service chatbot representing a professional audit and advisory firm. 
                Always respond as if you are a trusted and knowledgeable employee of the firm, never as a third party. 
                Your tone should be professional, respectful, and client-focused, aiming to provide clear, concise information.
                Use only the information below as the basis for your answers:
                
                {company_info}
                
                User Question: {user_message}"""
                
                # Generate response using the API
                response_obj = model.generate_content(prompt)
                
                if hasattr(response_obj, 'text'):
                    gemini_response = response_obj.text
                else:
                    gemini_response = "Sorry, I encountered an error generating a response."
                
                styled_response = get_styled_response(gemini_response)
                response = {"response": styled_response}
                
            except Exception as api_error:
                print(f"API Error: {api_error}")
                response = {"error": f"API error: {str(api_error)}"}
            
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"Server Error: {e}")
            response = {"error": f"Server error: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
