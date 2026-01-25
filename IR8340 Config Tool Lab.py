from flask import Flask, render_template, request
from all_models import CoreNetwork
from generator import generate_core_config  # your existing generator

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    config_text = ""
    if request.method == "POST":
        # collect the form data
        core = CoreNetwork(
            hostname=request.form["hostname"],
            loopback0=request.form["loopback0"],
            loopback1=request.form["loopback1"],
            hub_slice=request.form["hub_slice"],
            city=request.form["city"],
            state=request.form["state"],
            location_type=request.form["location_type"]
        )
        # generate the core config
        config_text = generate_core_config(core)

    return render_template("index.html", config_text=config_text)

if __name__ == "__main__":
    app.run(debug=True)
