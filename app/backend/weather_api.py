"""
Get weather from station along with health and ready checks.

"""

import os
import json
import redis
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

try:
    redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)
except redis.exceptions.ConnectionError as error:
    redis_client = None

@app.route("/weather")
def weather():
    """
    Call api.weather.gov station
    check if last request was more than 10 min ago
    if more call api and store data in redis.
    """
    city = request.args.get("city", "Intercourse")
    cache_key = f"weather:{city.lower()}"

    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))

    try:
        resp = requests.get(
            "https://api.weather.gov/stations/KLNS/observations/latest",
             timeout=5
           )
        resp.raise_for_status()
        data = resp.json()

        redis_client.setex(cache_key, 600, json.dumps(data))
        return jsonify(data), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504

    except requests.exceptions.RequestException as request_error:
        app.logger.error("Weather API failed: %s", request_error)
        return jsonify({"error": "Failed to fetch weather data"}), 502

@app.route("/healthz")
def liveness_check():
    """
    Health check for pod
    """
    return jsonify({"status" : "Healthy" }) , 200

@app.route("/ready")
def readiness_check():
    """
    readniess probe to see if redis is connected.
    """
    if not redis_client:
        return jsonify({"status": "not ready", "reason": "redis client not initialized" }), 503

    try:
        #PING REDIS
        redis_client.ping()
        return jsonify({"status": "ready" }), 200
    except redis.exceptions.ConnectionError as redis_ping_error:
        print("Readiness check failed to connect to Redis:", redis_ping_error)
        return jsonify({"status": "not ready", "reason" : "redis connection failed"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
