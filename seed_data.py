from db import classes
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone('Asia/Kolkata')

def seed_classes():
    now = datetime.now(IST)
    classes.extend([
        {
            "id": 1,
            "name": "Yoga",
            "datetime": now + timedelta(days=1, hours=7),
            "instructor": "Anjali",
            "available_slots": 10
        },
        {
            "id": 2,
            "name": "Zumba",
            "datetime": now + timedelta(days=1, hours=9),
            "instructor": "Rahul",
            "available_slots": 8
        },
        {
            "id": 3,
            "name": "HIIT",
            "datetime": now + timedelta(days=1, hours=18),
            "instructor": "Sara",
            "available_slots": 5
        }
    ])