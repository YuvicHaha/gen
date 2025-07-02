from flask import Flask, jsonify, request
import requests
import random
import string
from colorama import init
import os

init()

app = Flask(__name__)

def generate_username(length=10):
    allowed_chars = string.ascii_lowercase + string.digits + "_"
    return ''.join(random.choices(allowed_chars, k=length))

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        code = data.get("code")
        message = data.get("message", "OK")
        return {
            "username": username,
            "code": code,
            "message": message
        }
    except Exception as e:
        return {
            "username": username,
            "error": str(e)
        }

@app.route("/")
def home():
    return "✅ Roblox Username Checker API is running!"

@app.route("/generate", methods=["GET"])
def generate_and_check():
    count = int(request.args.get("count", 1))
    length = int(request.args.get("length", 10))

    results = []
    for _ in range(count):
        username = generate_username(length)
        result = check_username(username)
        results.append(result)

        if result.get("code") == 0:
            with open("valid.txt", "a") as f:
                f.write(username + "\n")

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
