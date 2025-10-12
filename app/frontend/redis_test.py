import redis, os
from flask import Flask

app = Flask(__name__)

# connect using environment variable or default
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

@app.route('/cache')
def cache_example():
    # write
    r.setex('greeting', 10, 'Hello, World!')  # expires in 60s
    # read
    message = r.get('greeting')
    return message or "Cache expired!"

if __name__ == '__main__':
   app.run(debug=True) 
