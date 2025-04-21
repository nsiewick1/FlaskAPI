from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)


API_TOKEN = "supersecrettoken123"


capital_timezones = {
    "Washington": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "New Delhi": "Asia/Kolkata",
    "Canberra": "Australia/Sydney",
    "Ottawa": "America/Toronto",
    "Beijing": "Asia/Shanghai",
    "Brasília": "America/Sao_Paulo"
}

# Decorator for token-based access control
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

# Main endpoint that returns time info based on capital
@app.route('/api/time', methods=['GET'])
@token_required
def get_local_time():
    capital = request.args.get("capital")
    if not capital:
        return jsonify({"error": "Please provide a capital query parameter."}), 400

    timezone = capital_timezones.get(capital)
    if not timezone:
        return jsonify({"error": f"'{capital}' not found in database."}), 404

    local_time = datetime.now(pytz.timezone(timezone))
    offset = local_time.strftime('%z')

    return jsonify({
        "capital": capital,
        "local_time": local_time.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": f"{offset[:3]}:{offset[3:]}"
    })

# Demo endpoint (not protected)
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
