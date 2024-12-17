import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_BASE_URL = "http://example.com/api"  # Replace with your actual REST API endpoint


def fetch_data_from_api(endpoint):
    response = requests.get(f"{API_BASE_URL}/{endpoint}")
    return response.json() if response.status_code == 200 else None


def send_data_to_api(endpoint, data):
    response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
    return response.json() if response.status_code == 201 else None


def update_data_on_api(endpoint, data):
    response = requests.put(f"{API_BASE_URL}/{endpoint}", json=data)
    return response.json() if response.status_code == 200 else None


def delete_data_from_api(endpoint):
    response = requests.delete(f"{API_BASE_URL}/{endpoint}")
    return response.status_code == 204


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch_data", methods=["GET"])
def fetch_data():
    endpoint = "items"  # Specify your data endpoint
    data = fetch_data_from_api(endpoint)
    if data:
        return jsonify(data), 200
    return jsonify({"message": "Data not found"}), 404


@app.route("/add_data", methods=["POST"])
def add_data():
    new_data = request.json
    endpoint = "items"  # Specify your data endpoint
    data = send_data_to_api(endpoint, new_data)
    if data:
        return jsonify(data), 201
    return jsonify({"message": "Failed to add data"}), 400


@app.route("/update_data/<int:item_id>", methods=["PUT"])
def update_data(item_id):
    updated_data = request.json
    endpoint = f"items/{item_id}"  # Specify your data endpoint
    data = update_data_on_api(endpoint, updated_data)
    if data:
        return jsonify(data), 200
    return jsonify({"message": "Failed to update data"}), 400


@app.route("/delete_data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id):
    endpoint = f"items/{item_id}"  # Specify your data endpoint
    if delete_data_from_api(endpoint):
        return jsonify({"message": "Data deleted successfully"}), 204
    return jsonify({"message": "Failed to delete data"}), 400


if __name__ == "__main__":
    app.run(debug=True)
