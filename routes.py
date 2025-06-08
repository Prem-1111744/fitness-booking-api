from flask import Blueprint, request, jsonify
from models import get_all_classes, get_class_by_id, reduce_class_slot, create_booking, get_bookings_by_email
from utils import convert_to_timezone

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/classes', methods=['GET'])
def list_classes():
    timezone = request.args.get('timezone', 'Asia/Kolkata')
    classes = get_all_classes()
    for cls in classes:
        cls['datetime'] = convert_to_timezone(cls['datetime'], timezone)
    return jsonify(classes)

@booking_bp.route('/book', methods=['POST'])
def book_class():
    data = request.json
    required = ['class_id', 'client_name', 'client_email']
    if not all(key in data for key in required):
        return jsonify({'error': 'Missing fields'}), 400

    cls = get_class_by_id(data['class_id'])
    if not cls:
        return jsonify({'error': 'Class not found'}), 404

    if cls['available_slots'] <= 0:
        return jsonify({'error': 'No slots available'}), 400

    reduce_class_slot(data['class_id'])
    create_booking(data['class_id'], data['client_name'], data['client_email'])
    return jsonify({'message': 'Booking successful'})

@booking_bp.route('/bookings', methods=['GET'])
def view_bookings():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    bookings = get_bookings_by_email(email)
    return jsonify(bookings)