import pandas as pd


rooms = pd.read_csv("bookings/data/rooms.csv",
    dtype={
     'id': int,
     'name': str   
    })


keys = pd.read_csv("bookings/data/keys.csv",
    dtype={
     'id': int,
     'pubkey': str,
     'privkey': str,
     'tokens': int
    })


bookings = lambda: pd.read_csv("bookings/data/bookings.csv",
    dtype={
     'roomId': int,
     'userId': int,
     'year': int,
     'month': int,
     'day': int,
     'starttime': str,
     'eventId': int
    })

def generate_military_time(s: int):
    if len(str(s)) == 1:
        return f'0{s}00'
    return f'{s}00'

times = list(map(generate_military_time, range(24)))


# print(rooms.head())
# print(keys.head())
# print(bookings.head())
# print(times)