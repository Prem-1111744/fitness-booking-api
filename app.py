from flask import Flask, request, jsonify
from db import classes, bookings, init_db
from seed_data import seed_classes
from utils import convert_to_timezone
import logging
import pytz


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
init_db()
seed_classes()

@app.route('/classes', methods=['GET'])
def list_classes():
    timezone = request.args.get('timezone', 'Asia/Kolkata')

    try:
        pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        logging.warning("Invalid timezone requested: %s", timezone)
        return jsonify({"error": f"Unknown timezone: {timezone}"}), 400

    result = []
    for cls in classes:
        result.append({
            "id": cls['id'],
            "name": cls['name'],
            "datetime": convert_to_timezone(cls['datetime'], timezone),
            "instructor": cls['instructor'],
            "available_slots": cls['available_slots']
        })

    logging.info("Returned %d classes in timezone %s", len(result), timezone)
    return jsonify(result), 200

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()

    required_fields = ['class_id', 'client_name', 'client_email']
    if not all(field in data for field in required_fields):
        logging.warning("Booking failed: missing required fields.")
        return jsonify({"error": "Missing required fields"}), 400

    class_id = data["class_id"]
    name = data["client_name"]
    email = data["client_email"]

    for cls in classes:
        if cls["id"] == class_id:
            if cls["available_slots"] > 0:
                cls["available_slots"] -= 1
                booking = {
                    "class_id": class_id,
                    "client_name": name,
                    "client_email": email
                }
                bookings.append(booking)
                logging.info("Booking successful for %s in class %s", name, class_id)
                return jsonify({'message':'booking successful'}), 200
            else:
                logging.warning("Booking failed: class %s is full", class_id)
                return jsonify({"error": "Class is full"}), 400

    logging.warning("Booking failed: class not found")
    return jsonify({"error": "Class not found"}), 400

@app.route('/bookings', methods=['GET'])
def get_user_bookings():
    email = request.args.get("email")
    if not email:
        logging.warning("Fetching bookings failed: email missing")
        return jsonify({"error": "Email is required"}), 400

    user_bookings = [b for b in bookings if b["client_email"].lower() == email.lower()]
    logging.info("Found %d bookings for %s", len(user_bookings), email)
    if not user_bookings:
        return jsonify({"message": "no bookings till now"}), 200
    return jsonify(user_bookings), 200

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed. Please use the correct HTTP method."}), 405

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "The requested URL was not found on the server. Please check your spelling and try again."}), 404

if __name__ == '__main__':
    app.run(debug=True)