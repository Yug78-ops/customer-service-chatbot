from http.server import BaseHTTPRequestHandler
import json

ALLOWED_ORIGIN = "*"              # or put your exact site, e.g. https://tpadhikari.com
ALLOW_IFRAME  = "frame-ancestors *"   # or "frame-ancestors https://tpadhikari.com"

class handler(BaseHTTPRequestHandler):

    def _common_headers(self):
        # CORS
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        # >>> these two lines let WordPress embed the page <<<
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.send_header("Content-Security-Policy", ALLOW_IFRAME)

    def do_OPTIONS(self):
        self.send_response(200)
        self._common_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._common_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # (rest of your GET logic …)

    def do_POST(self):
        self.send_response(200)
        self._common_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # (rest of your POST logic …)
