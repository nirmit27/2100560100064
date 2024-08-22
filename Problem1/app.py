""" Problem 1 : Average Calculator Microservice """

import os
import time
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

WINDOW_SIZE = 10
TEST_SERVER_URL = "http://20.244.56.144/test/"
TIMEOUT = 0.5
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzI0MTYyMDk5LCJpYXQiOjE3MjQxNjE3OTksImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjYxYWY2Mjk4LTVhYmQtNGMzZi04OTBlLTI0YTVjMTAzOTBhMSIsInN1YiI6Im1pc2hyYW5pcm1pdDI3QGdtYWlsLmNvbSJ9LCJjb21wYW55TmFtZSI6ImZhc3QtYXBwIiwiY2xpZW50SUQiOiI2MWFmNjI5OC01YWJkLTRjM2YtODkwZS0yNGE1YzEwMzkwYTEiLCJjbGllbnRTZWNyZXQiOiJIR2ZxRmlKdVVVc2FhV1JGIiwib3duZXJOYW1lIjoiTmlybWl0IE1pc2hyYSIsIm93bmVyRW1haWwiOiJtaXNocmFuaXJtaXQyN0BnbWFpbC5jb20iLCJyb2xsTm8iOiIyMTAwNTYwMTAwMDY0In0.6f0C8xyveYk4ztXX8MWbEAUn_LZThi7kX6DVD8aLT5g"

window: list = []

def fetch_numbers(number_id):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    try:
        response = requests.get(f"{TEST_SERVER_URL}/{number_id}", headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.exceptions.RequestException:
        pass
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
