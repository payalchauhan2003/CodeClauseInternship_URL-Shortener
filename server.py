from flask import Flask, request, jsonify, redirect
import hashlib
import base64

app = Flask(__name__)

# Dictionary to store mappings between long URLs and short codes
url_map = {}
# Dictionary to store mappings between short codes and long URLs
short_to_long = {}
# Base URL for shortened links
base_url = "http://localhost:5000/"
# ID counter for generating unique short codes
id_counter = 1


def generate_short_code():
    global id_counter
    # Convert the current ID counter to a base62 string to generate a unique short code
    short_code = to_base62(id_counter)
    id_counter += 1
    return short_code


def to_base62(num):
    # Convert a number to a base62 string
    base62_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while num > 0:
        remainder = num % 62
        result.append(base62_chars[remainder])
        num //= 62
    return ''.join(result[::-1])


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('url')

    # Check if the long URL is already in the map
    if long_url in url_map:
        short_code = url_map[long_url]
        return jsonify(short_url=base_url + short_code)

    # Generate a unique short code
    short_code = generate_short_code()

    # Store the mapping between the long URL and the short code
    url_map[long_url] = short_code
    # Store the reverse mapping between the short code and the long URL
    short_to_long[short_code] = long_url

    # Return the shortened URL as JSON
    return jsonify(short_url=base_url + short_code)


@app.route('/<short_code>')
def expand_url(short_code):
    # Retrieve the long URL from the short code
    long_url = short_to_long.get(short_code)

    if long_url:
        return redirect(long_url)
    else:
        return "Short URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
