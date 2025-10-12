@app.route('/cache')
def cache_example():
    # write
    r.setex('greeting', 60, 'Hello, World!')  # expires in 60s
    # read
    message = r.get('greeting')
    return message or "Cache expired!"

