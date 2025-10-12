from flask import Flask, request, jsonify
import requests, redis, os, json, time

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

@app.route("/weather")
def weather():
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
       return jsonify(data)
           
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Weather API failed: {e}")
        return jsonify({"error": "Failed to fetch weather data"}), 502   
   
    if resp.status_code == requests.codes.ok:
    	data = resp.json()
    	r.setex(cache_key, 600, json.dumps(data))  # cache 10 min
    	return jsonify(data)
    else:
    	error = resp.json()
    	r.setex(cache_key,10,json.dumps(error)) # 10 sec
    	return jsonify(error)
    	
if __name__ == '__main__':
   app.run(debug=True) 
