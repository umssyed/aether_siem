import os
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
from .database import SessionLocal
from .model import HistoricalUsage

load_dotenv()
routes = Blueprint('routes', __name__)
API_KEY = os.getenv("SUPABASE_KEY")

# POST: Nightwatcher logs data
@routes.route("/log", methods=["POST"])
def log_data():
    client_key = request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        print(f"[INFO] Log received: {data}")
        session = SessionLocal()
        record = HistoricalUsage(
            tenant_id = "umssyed",
            timestamp =  datetime.utcnow(),
            hostname = data.get("hostname", "Unknown"),
            process_name = data.get("app_name", "Unknown"),
            cpu = float(data.get("cpu_percentage", 0.0)),
            mem = float(data.get("memory", 0.0)),
            reason = data.get("reason", "")
        )
        session.add(record)
        session.commit()
        session.close()
        return jsonify({"status":"saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET: Dashboard receive data
@routes.route("/api/historical", methods=["GET"])
def get_historical():
    try:
        session = SessionLocal()
        results = session.query(HistoricalUsage).order_by(HistoricalUsage.timestamp.desc()).limit(50).all()
        session.close()

        data = [
            {
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": r.hostname,
                "process_name": r.process_name,
                "cpu": r.cpu,
                "mem": r.mem,
                "reason": r.reason
            }
            for r in results
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

