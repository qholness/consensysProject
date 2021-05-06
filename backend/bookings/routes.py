from bookings import app
from bookings.data import bookings, keys, rooms, times
from flask import request
import time

@app.route("/get-rooms")
def get_rooms():
    return rooms.to_json(index=True, orient="records")


@app.route("/get-users")
def get_users():
    return keys.to_json(index=True, orient="records")


@app.route("/my-bookings")
def my_bookings():
    from bookings.services import inject_room_names
    user_id = request.args.get("userId")

    if(user_id):
        user_id = int(user_id)
        current_bookings = bookings()
        current_bookings = current_bookings[current_bookings["userId"] == user_id]
        current_bookings = inject_room_names(current_bookings)
        return current_bookings.to_json(index=True, orient="records")


@app.route("/cancel-booking")
def cancel_booking():
    eventId = request.args.get('eventId')
    
    current_bookings = bookings()

    current_bookings = current_bookings.query(f"eventId != {int(eventId)}")

    current_bookings.to_csv(
        './bookings/data/bookings.csv',
        index=False)
    
    return f"Canceled [{eventId}]"


@app.route("/get-availability")
def get_booking_availability():
    from bookings.services import inject_room_names, inject_available_times
    room_id = request.args.get("roomId")
    year = request.args.get("year")
    month = request.args.get("month")
    day = request.args.get("day")
 
    if room_id:
        room_id, year, month, day = list(map(int,
            (room_id, year, month, day)))
        
        current_bookings = bookings()

        # Filter by roomId and date
        query = f"""roomId == {room_id} & year == {year} & month == {month} & day == {day}""" 
        current_bookings = current_bookings.query(query)

        # Add room names for frontend readability
        current_bookings = inject_room_names(current_bookings)
        
        # Add bool status for frontend manipulation
        current_bookings['isAvailable'] = False

        # Inject missing times as "available"
        current_bookings = inject_available_times(
            current_bookings, {
                'roomId': room_id,
                'year': year,
                'month': month,
                'day': day
            })
        return current_bookings.to_json(index=True, orient="records")


@app.route("/book-room")
def book_a_room():
    # Validate availability and book if available
    userId = int(request.args.get('userId'))
    roomId = int(request.args.get('roomId'))
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    day = int(request.args.get('day'))
    starttime = request.args.get('starttime')
    current_bookings = bookings()
    query = f"""roomId == {roomId} & year == {year} & month == {month} & day == {day} & starttime == {starttime}"""
    if current_bookings.query(query).empty:
        # Generate eventId
        eventId = 0
        while eventId in current_bookings['eventId'].values:
            eventId += 1
        
        current_bookings = current_bookings.append({
            'userId': userId,
            'roomId': roomId,
            'year': year,
            'month': month,
            'day': day,
            'starttime': starttime,
            'eventId': eventId
        }, ignore_index=True)

        # Save to CSV
        current_bookings.to_csv(
            './bookings/data/bookings.csv',
            index=False)
        
        return "Room booked!"
    
    else:
    
        return "Room unavailable"

