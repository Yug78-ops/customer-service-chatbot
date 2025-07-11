from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
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
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Get API key from environment
            api_key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
            
            if not api_key or not GENAI_AVAILABLE:
                response = {
                    "response": "<span class='bot-response-text'>I apologize, but the AI service is currently unavailable. Please ensure your API key is properly configured in Vercel environment variables and try again later.</span>"
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Company information (you should replace this with your actual content)
            company_info = """
            We are a professional audit and advisory firm committed to providing exceptional services to our clients. 
            Our services include financial audits, tax advisory, business consulting, and risk management.
            We maintain the highest standards of integrity, objectivity, and professional excellence.
            
            Please replace this placeholder with your actual company services content from the PDF.
            """
            
            # Create prompt
            prompt = f"""You are a customer service chatbot representing a professional audit and advisory firm. Always respond as if you are a trusted and knowledgeable employee of the firm, never as a third party. Your tone should be professional, respectful, and client-focused, aiming to provide clear, concise, and accurate information without compromising quality. Maintain the highest standards of confidentiality and never disclose any sensitive, proprietary, or internal information about the firm, its clients, or its operations. All responses must align with the firm's values of integrity, objectivity, and service excellence. If a question falls outside the scope of the information provided, respond appropriately and indicate that the inquiry will be referred to the relevant team. Use only the information given below as the basis for your answers, and ensure that every response reflects the commitment to ethical conduct and client trust that defines a reputable audit firm. Always format responses using concise, single-line spacing without unnecessary line breaks or paragraph gaps. Answer questions based on the following information:\n\n{company_info}\n\nUser Question: {user_message}"""
            
            # Generate response
            ai_response = model.generate_content(prompt)
            
            if hasattr(ai_response, 'text'):
                response_text = ai_response.text
            else:
                response_text = "Sorry, I encountered an error generating a response."
            
            # Style the response
            styled_response = f"<span class='bot-response-text'>{response_text}</span>"
            
            response = {"response": styled_response}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": f"An error occurred: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
