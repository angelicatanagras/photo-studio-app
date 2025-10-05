from datetime import datetime, timedelta
from ..models.booking import Booking
from ..database import fetch_all


def format_currency(amount):
    return f"${amount:.2f}"


def calculate_duration(start_time, end_time):
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    duration = end_time - start_time
    return duration.total_seconds() / 3600


def is_time_slot_available(photographer_id, event_date, exclude_booking_item_id=None):
    query = """
        SELECT bi.* FROM booking_items bi
        JOIN bookings b ON bi.booking_id = b.id
        WHERE bi.photographer_id = %s
        AND bi.event_start = %s
        AND b.status IN ('confirmed', 'pending')
    """
    params = [photographer_id, event_date]

    if exclude_booking_item_id:
        query += " AND bi.id != %s"
        params.append(exclude_booking_item_id)

    conflicting_bookings = fetch_all(query, tuple(params))
    return len(conflicting_bookings) == 0


def validate_booking_date(event_date):
    errors = []

    if isinstance(event_date, datetime):
        event_date = event_date.date()

    if isinstance(event_date, str):
        try:
            event_date = datetime.fromisoformat(event_date).date()
        except ValueError:
            errors.append("Invalid date format")
            return errors

    if event_date < datetime.now().date():
        errors.append("Booking cannot be in the past")

    return errors