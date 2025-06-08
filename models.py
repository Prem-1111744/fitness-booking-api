from db import classes, bookings

def get_all_classes():
    return classes

def book_class(class_id, name, email):
    for cls in classes:
        if cls['id'] == class_id and cls['available_slots'] > 0:
            cls['available_slots'] -= 1
            booking = {
                "id": len(bookings) + 1,
                "class_id": class_id,
                "client_name": name,
                "client_email": email
            }
            bookings.append(booking)
            return booking
    return None

def get_bookings_by_email(email):
    return [b for b in bookings if b['client_email'].lower() == email.lower()]