from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
from io import StringIO
from flask_cors import CORS  # Import CORS
import bleach

app = Flask(__name__, static_folder="static")  # Specify static folder
CORS(app)  # Enable CORS for all routes

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Load data from PDF file
PDF_FILE_PATH = "company_services.pdf"  # Relative path, same directory as app.py

def load_pdf_content(file_path):
    """Extracts text content from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except FileNotFoundError:
        print(f"Error: PDF file not found at '{file_path}'")
        return None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text

def get_styled_response(text):
    # Sanitize the HTML to prevent XSS vulnerabilities
    sanitized_text = bleach.clean(text, tags=['p', 'br', 'span'], attributes={'span': ['style', 'class']})
    styled_text = f"<span class='bot-response-text'>{sanitized_text}</span>"
    return styled_text

company_info = load_pdf_content(PDF_FILE_PATH)

if company_info is None:
    print("Failed to load company information from PDF.")
    company_info = "I am unable to answer questions about the company services because the information could not be loaded." #Or some default message
else:
    print("Company information loaded successfully from PDF.")


# Logo colors (Consider reading these from a config file or environment)
logo_primary_color = "#007bff"  # Example: Blue
logo_secondary_color = "#f8f9fa"  # Example: Light Gray

def get_styled_response(text):
    """
    Applies styling to the Gemini response based on logo colors.
    Now just returns a styled span; actual styling should be in CSS.
    """
    styled_text = f"<span class='bot-response-text'>{text}</span>" # Class for CSS styling
    return styled_text

# Route to serve the index.html file
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')  # Serve index.html

# Route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Route to serve CSS files
@app.route('/static/css/<path:filename>')
def css_files(filename):
    return send_from_directory('static/css', filename)

# Route to serve JS files
@app.route('/static/js/<path:filename>')
def js_files(filename):
    return send_from_directory('static/js', filename)

# Route to serve image files
@app.route('/static/images/<path:filename>')
def image_files(filename):
    return send_from_directory('static/images', filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Construct a prompt that includes the company information
        prompt = f"""You are a customer service chatbot representing a professional audit and advisory firm. Always respond as if you are a trusted and knowledgeable employee of the firm, never as a third party. Your tone should be professional, respectful, and client-focused, aiming to provide clear, concise, and accurate information without compromising quality. Maintain the highest standards of confidentiality and never disclose any sensitive, proprietary, or internal information about the firm, its clients, or its operations. All responses must align with the firm’s values of integrity, objectivity, and service excellence. If a question falls outside the scope of the information provided, respond appropriately and indicate that the inquiry will be referred to the relevant team. Use only the information given below as the basis for your answers, and ensure that every response reflects the commitment to ethical conduct and client trust that defines a reputable audit firm. Always format responses using concise, single-line spacing without unnecessary line breaks or paragraph gaps. Answer questions based on the following information:\n\n{company_info}\n\nUser Question: {user_message}"""

        response = model.generate_content(prompt)

        if hasattr(response, 'text'):
            gemini_response = response.text
        else:
            gemini_response = "Sorry, I encountered an error generating a response."
            print(f"Error generating response: {response}")

        styled_response = get_styled_response(gemini_response)
        return jsonify({"response": styled_response})

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500


# For local development
if __name__ == '__main__':
    app.run(debug=True)

# For Vercel deployment
def application(environ, start_response):
    return app(environ, start_response)