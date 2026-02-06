"""
Get weather from station along with health and ready checks.

"""

import os
import redis
import requests
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from zipcodes import load_zipcodes, zipcode_lookup

load_zipcodes()

app = Flask(__name__)

CORS(app, resources={r"/weather": {"origins": "*"}})

try:
    redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)
except redis.exceptions.ConnectionError as error:
    redis_client = None
# user-agent needed to prevent throttle
session = requests.Session()
session.headers.update({
    "User-Agent" : "weather-app (mattmootz@gmail.com)"
})


def api_call(url):
    """
    Docstring for api_call
    utility function to call url and return json body
    :param url: url to call api with
    returns data as json
    """
    try:
        resp = session.get(
            url,
             timeout=5
           )
        resp.raise_for_status()
        data = resp.json()

        return data, 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504

    except requests.exceptions.RequestException as request_error:
        app.logger.error("Weather API failed: %s", request_error)
        return jsonify({"error": "Failed to fetch weather data"}), 502

@app.route("/weather")
def weather():
    """
    Call api.weather.gov station
    check if zipcode is in redis if get data from weather.gov
    check if last request was more than 10 min ago
    if more call api and store data in redis.
    """

    zipcode = request.args.get("zipcode")

    if not zipcode:
        abort(400, description="zipcode is required")

    if not zipcode.isdigit() or len(zipcode) !=5:
        abort(400, description="invalid zipcode")


    lat, lon = zipcode_lookup(zipcode)
    base_url = "https://api.weather.gov/"
    get_lat_long = "points/"
    completed_url = base_url + get_lat_long + str(lat) + "," + str(lon)

    data, status = api_call(completed_url)
    if status != 200:
        return jsonify({"error": "Request failed with error code"}), status

    get_station = data['properties']['observationStations']

    stations, status = api_call(get_station)
    if status != 200:
        return jsonify({"error": "Request failed with error code"}), status

    first_station_identifier = stations['features'][00]['properties']['stationIdentifier']
    weather_header = "stations/"
    weather_footer = "/observations/latest"
    get_station_weather = base_url + weather_header + first_station_identifier + weather_footer

    current_weather, status = api_call(get_station_weather)

    if status == 200:
        # city = request.args.get("city", "Intercourse")
        # cache_key = f"weather:{city.lower()}"

        # cached = redis_client.get(cache_key)
        # if cached:
        #     return jsonify(json.loads(cached))
        return current_weather
    else:
        return jsonify({"error" : "request failed checking current weather" }), status


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
