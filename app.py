from flask import Flask, send_from_directory
import os

# Create a simple app that just serves static files
app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(path):
        return send_from_directory(".", path)
    else:
        return send_from_directory(".", "index.html")

# For Vercel deployment
app = app
