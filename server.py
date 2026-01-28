import os
import threading
import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from flask_cors import CORS
from lib.generator import generate_vrf_config

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

@app.route("/update_vrf", methods=["POST"])
def update_vrf():
    try:
        vrfs = request.get_json()
        print("Received VRF payload:", vrfs)

        if not vrfs:
            return jsonify({"error": "No VRF data received"}), 400

        configs = []

        for vrf in vrfs:
            network_name = vrf.get("network")
            if not network_name:
                continue  # skip empty entries

            template_name = f"{network_name.lower()}.j2"
            template_path = os.path.join("Templates", "IPL", "VRFs", template_name)

            # Check file exists for debugging
            if not os.path.exists(template_path):
                error_msg = f"Template not found for VRF '{network_name}' at {template_path}"
                print(error_msg)
                return jsonify({"error": error_msg}), 400

            # Prepare core object for template rendering
            core = {"hub_slice": vrf.get("hub_slice", "")}

            # Generate VRF config
            try:
                config_text = generate_vrf_config(
                    core=core,
                    vrf=vrf,
                    template_name=template_name  # only filename, Jinja loader handles path
                )
                configs.append(config_text)
            except Exception as e:
                error_msg = f"Error generating VRF '{network_name}': {e}"
                print(error_msg)
                return jsonify({"error": error_msg}), 500

        # Return all VRFs joined together as a single string
        return jsonify({"config": "\n".join(configs)})

    except Exception as e:
        print("Unexpected error in /update_vrf:", e)
        return jsonify({"error": str(e)}), 500
    
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
