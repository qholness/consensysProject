def get_room_name_by_id(_id):
    from bookings.data import rooms
    return rooms.set_index('id').iloc[int(_id)]['name']

def inject_room_names(data):
    from bookings.data import rooms
    return data.set_index('roomId').join(rooms.set_index('id')).reset_index()

def inject_available_times(data, search_data: dict):
    from bookings.data import times

    room_id = search_data.get('roomId')
    
    for idx, t in enumerate(times):
        if t not in data['starttime'].values:
            row = {
                'roomId': room_id,
                'userId': None,
                'year': search_data.get('year'),
                'month': search_data.get('month'),
                'day': search_data.get('day'),
                'starttime': str(t),
                'name': get_room_name_by_id(room_id),
                'isAvailable': True,
                'eventId': None
            }
            data = data.append(row, ignore_index=True)
    return data.sort_values(by=[
        'starttime'
    ])