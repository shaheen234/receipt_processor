from flask import Flask, request, jsonify
import uuid
import math
from datetime import datetime

app = Flask(__name__)

# In-memory store for receipts and points
receipts = {}
points_store = {}

def calculate_points(receipt):
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer_name = receipt.get("retailer", "")
    points += sum(c.isalnum() for c in retailer_name)

    # Rule 2: 50 points if the total is a round dollar amount
    total = float(receipt.get("total", 0))
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    # Rule 5: Points for item descriptions that are multiples of 3
    for item in items:
        description = item.get("shortDescription", "").strip()
        if len(description) % 3 == 0:
            price = math.ceil(float(item.get("price", 0)) * 0.2)
            points += price

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = receipt.get("purchaseDate", "")
    try:
        day = int(purchase_date.split("-")[-1])
        if day % 2 == 1:
            points += 6
    except (ValueError, IndexError):
        pass

    # Rule 7: 10 points if the purchase time is between 2:00pm and 4:00pm
    purchase_time = receipt.get("purchaseTime", "")
    try:
        time = datetime.strptime(purchase_time, "%H:%M").time()
        if datetime.strptime("14:00", "%H:%M").time() <= time < datetime.strptime("16:00", "%H:%M").time():
            points += 10
    except ValueError:
        pass

    return points

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    try:
        receipt = request.json
        receipt_id = str(uuid.uuid4())
        points = calculate_points(receipt)

        # Store receipt and points in memory
        receipts[receipt_id] = receipt
        points_store[receipt_id] = points

        return jsonify({"id": receipt_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    try:
        if receipt_id in points_store:
            return jsonify({"points": points_store[receipt_id]}), 200
        else:
            return jsonify({"error": "Receipt ID not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
