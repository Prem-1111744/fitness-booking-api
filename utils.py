import pytz
from dateutil.parser import parse

def convert_to_timezone(dt, tz_name):
    if isinstance(dt, str):
        dt = parse(dt)
    local_tz = pytz.timezone(tz_name)
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    local_dt = dt.astimezone(local_tz)
    return local_dt.strftime('%Y-%m-%d %I:%M %p')