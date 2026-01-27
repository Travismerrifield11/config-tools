import os
import threading
import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from all_models import (
    CoreNetwork,
    WANConfig,
    RouterWANs,
    VRFConfig,
    PortConfig
)

from generator import (
    generate_core_config,
    generate_wan_config,
    generate_vrf_config,
    generate_ports_config
)

    
# ---- Flask setup ----
app = Flask(__name__)
CORS(app)  # allow all origins

# ---- Route to index.html ----
@app.route("/")
def index():
    return send_from_directory("website", "index.html")


# ---- Serve static files (CSS, JS) ----
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

# ---- Core config endpoint ----
@app.route("/generate/core", methods=["POST"])
def generate_core():
    data = request.json
    core = CoreNetwork(**data)
    config = generate_core_config(core)
    return jsonify({"config": config})

# ---- WAN config endpoint ----
@app.route("/generate/wan", methods=["POST"])
def generate_wan():
    data = request.get_json()

    if not isinstance(data, list):
        return "Invalid WAN payload", 400

    wans = []
    for row in data:
        if not row.get("circuit"):
            continue

        wans.append(WANConfig(
            circuit_id=row.get("circuit"),
            bandwidth=row.get("bandwidth"),
            ip_address=row.get("ip"),
            media_type=row.get("media_type")
        ))

    router_wans = RouterWANs(wans=wans)
    return generate_wan_config(router_wans)
    
# ---- VRF config endpoint ----
@app.route("/generate/vrf", methods=["POST"])
def generate_vrf():
    data = request.get_json()

    if not isinstance(data, list):
        return "Invalid VRF payload", 400

    vrfs = []
    for row in data:
        if not row.get("name"):
            continue

        vrfs.append(VRFConfig(
            name=row.get("name"),
            rd=row.get("rd"),
            rt=row.get("rt")
        ))

    return generate_vrf_config(vrfs)

    
# ---- PORTS config endpoint ----    
@app.route("/generate/ports", methods=["POST"])
def generate_ports():
    data = request.get_json()

    if not isinstance(data, list):
        return "Invalid ports payload", 400

    ports = []
    for row in data:
        if not row.get("interface"):
            continue

        ports.append(PortConfig(
            interface=row.get("interface"),
            ip=row.get("ip"),
            description=row.get("description"),
            media_type=row.get("media_type")
        ))

    return generate_ports_config(ports)


# ---- Auto-open browser ----
def open_browser():
    url = "http://127.0.0.1:5000/"
    webbrowser.open_new(url)

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
