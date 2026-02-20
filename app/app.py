import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello (default)\n")
API_KEY = os.getenv("API_KEY", "no-key")
APP_VERSION = os.getenv("APP_VERSION", "dev")

@app.get("/")
def home():
    return f"{APP_MESSAGE}version={APP_VERSION}\n"

@app.get("/health")
def health():
    return jsonify(status="ok", version=APP_VERSION)

@app.get("/secret")
def secret():
    return f"API_KEY={API_KEY}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
