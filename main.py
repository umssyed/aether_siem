from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/log", methods=["POST"])
def receive_log():
    log = request.json
    print(log)
    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)