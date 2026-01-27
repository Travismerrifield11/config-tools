import os
import threading
import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from lib.generator import (
    generate_core_config,
    generate_wan_config,
    generate_vrf_config,
    generate_ports_config
)

# ---------------- Flask Setup ----------------
app = Flask(__name__, static_folder="static")
CORS(app)

# ---------------- Serve UI ----------------
# Serve index.html from website folder
@app.route("/")
def index():
    return send_from_directory("website", "index.html")

# Serve other static files from /static/
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# ---------------- Generate Endpoints ----------------
# ---------------- Core ----------------
@app.route("/generate/core", methods=["POST"])
def generate_core():
    data = request.get_json()
    config = generate_core_config(data)
    return jsonify({"config": config})

# ---------------- Wan ----------------

@app.route("/generate/wan", methods=["POST"])
def generate_wan():
    data = request.get_json()
    config = generate_wan_config(data)
    print(config)
    return jsonify({"config": config})
    
# ---------------- VRF ----------------

@app.route("/generate/vrf", methods=["POST"])
def generate_vrf():
    data = request.get_json()
    config = generate_vrf_config(data)
    return jsonify({"config": config})
    
# ---------------- Ports ----------------

@app.route("/generate/ports", methods=["POST"])
def generate_ports():
    data = request.get_json()
    config = generate_ports_config(data)
    return jsonify({"config": config})

# ---------------- Auto-open Browser ----------------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, use_reloader=False)
