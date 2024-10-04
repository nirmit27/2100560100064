""" Problem 1 : Average Calculator Microservice """

import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)

WINDOW_SIZE = 10
TIMEOUT: float = 0.5
AUTH_TOKEN: str | None = os.environ.get("AUTH_TOKEN")
TEST_SERVER_URL: str | None = os.environ.get("TEST_SERVER_URL")

window: list = []


def fetch_numbers(number_id):
    try:
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        response = requests.get(
            f"{TEST_SERVER_URL}/{number_id}", headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.exceptions.RequestException as e:
        print(e)
    return []


@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    numbers = fetch_numbers(number_id)
    if not numbers:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    unique_numbers = list(set(numbers))
    window_prev_state = window.copy()

    for num in unique_numbers:
        if num not in window:
            if len(window) >= WINDOW_SIZE:
                window.pop(0)
            window.append(num)

    avg = sum(window) / len(window) if window else 0

    response = {
        "numbers": unique_numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window,
        "avg": round(avg, 2)
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
