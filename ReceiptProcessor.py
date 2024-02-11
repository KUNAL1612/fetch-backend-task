import logging
import math
from flask import Flask, jsonify, request
import uuid
import sqlite3

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('receipts.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema."""
    conn = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

def calculate_points(receipt):
    """Calculates the points earned for a given receipt based on predefined rules."""
    points = 0
    
    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt["retailer"])
    
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if float(receipt["total"]) == int(float(receipt["total"])):
        points += 50
        
    # Rule 3: 25 points if the total is a multiple of 0.25
    if float(receipt["total"]) % 0.25 == 0:
        points += 25
    
    # Rule 4: 5 points for every two items on the receipt
    points += len(receipt["items"]) // 2 * 5
    
    # Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to nearest integer
    for item in receipt["items"]:
        description_length = len(item["shortDescription"].strip())
        if description_length % 3 == 0:
            price = float(item["price"])
            points += math.ceil(price * 0.2)
    
    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_day = int(receipt["purchaseDate"].split("-")[-1])
    if purchase_day % 2 != 0:
        points += 6
    
    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt["purchaseTime"]
    hour = int(purchase_time.split(":")[0])
    minute = int(purchase_time.split(":")[1])
    if 14 <= hour < 16 and (hour != 14 or minute >= 1):
        points += 10
    
    return points

@app.route("/receipts/process", methods=["POST"])
def process_receipts():
    """Endpoint for submitting a receipt for processing."""
    try:
        receipt_data = request.json
        receipt_id = str(uuid.uuid4())

        points = calculate_points(receipt_data)

        # Log receipt processing
        logger.info(f"Receipt processed: ID={receipt_id}, Points={points}")

        conn = get_db_connection()
        conn.execute("INSERT INTO points (id, points) VALUES (?, ?)", (receipt_id, points))
        conn.commit()
        conn.close()

        response = {"id": receipt_id}
        return jsonify(response), 201
    except Exception as e:
        logger.error(f"Error processing receipt: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    """Endpoint for retrieving points awarded for a receipt."""
    try:
        conn = get_db_connection()
        result = conn.execute("SELECT points FROM points WHERE id=?", (receipt_id,)).fetchone()
        conn.close()

        if result is None:
            return jsonify({"error": "Receipt not found"}), 404
        
        points = result['points']

        # Log points retrieval
        logger.info(f"Points retrieved for receipt ID={receipt_id}: {points}")

        return jsonify({"points": points})
    except Exception as e:
        logger.error(f"Error retrieving points for receipt ID={receipt_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=10001)

