from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "Debug endpoint working!",
            "status": "success",
            "vercel_region": os.environ.get('VERCEL_REGION', 'not-set'),
            "vercel_env": os.environ.get('VERCEL_ENV', 'not-set'),
            "current_dir": os.getcwd()
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
