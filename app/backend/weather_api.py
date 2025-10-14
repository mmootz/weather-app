from flask import Flask, request, jsonify
import requests, redis, os, json, time

app = Flask(__name__)

    
@app.route("/weather")
def weather():
    
    try: 
        r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)
    except redis.exceptions.ConnectionError:
        return jsonify({"error": "Redis couldn't connect!"}), 500
    
    city = request.args.get("city", "Intercourse")
    cache_key = f"weather:{city.lower()}"

    cached = r.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
        
    try:
       resp = requests.get(
            "https://api.weather.gov/stations/KLNS/observations/latest",
            timeout=5
           )
       resp.raise_for_status()
       data = resp.json()
           
       r.setex(cache_key, 600, json.dumps(data))
       return jsonify(data), 200
           
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Weather API failed: {e}")
        return jsonify({"error": "Failed to fetch weather data"}), 502   
   

@app.route("/healthz")
def liveness_check():
    return "Healthy", 200


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
