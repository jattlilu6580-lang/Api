from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

API_KEY = "Demo"

# Credit Info
CREDIT = {
    "name": "ASUR",
    "developer": "@ASURPAPA",
    "contact": "https://t.me/ASUR_ABOUT",
    "footer": "Powered by ASUR"
}

# Database Load
DATA = []

with open("database.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    DATA = list(reader)


# Common Response Function
def response(status, result=None, message=None):
    data = {
        "status": status,
        "credit": CREDIT
    }

    if result is not None:
        data["result"] = result

    if message is not None:
        data["message"] = message

    return jsonify(data)


@app.route("/")
def home():
    return response(
        True,
        message="Aadhaar Search API Online"
    )


@app.route("/api")
def search():

    # API Key Check
    key = request.args.get("key")
    if key != API_KEY:
        return response(False, message="Invalid API Key"), 401

    # Aadhaar Check
    aadhar = request.args.get("aadhar")
    if not aadhar:
        return response(False, message="aadhar parameter required"), 400

    # Search
    for row in DATA:
        if row["aadharNumber"] == aadhar:
            return response(True, result=row)

    return response(False, message="Record not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
