from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Temporary storage for alerts
alerts = []

@app.route("/log", methods=["POST"])
def receive_log():
    log = request.json
    alerts.append(log)
    print("\nNew log received:")
    print(log)
    return jsonify({"status": "received"}), 200

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", alerts=alerts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)