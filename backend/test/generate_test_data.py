def generate_random_rooms():
    """Generate a list of 20 random room names"""
    from names import get_full_name
    
    name = get_full_name()
    room_names = [name]
    for i in range(21):
        while name in room_names:
            name = get_full_name()
        room_names.append(name)

    with open("./bookings/data/rooms.csv", "w+") as f:
        f.write("id,name\n")
        for  _id, name in enumerate(room_names):
            f.writelines(f"{_id},{name}\n")
    return room_names


def generate_random_public_private_keys(names):
    from cryptography.fernet import Fernet
    from time import time
    with open("./bookings/data/keys.csv", "w+") as data:
        data.write("id,pubkey,privkey,tokens\n")
        
        for _id, name in enumerate(names):
            key = Fernet.generate_key()
            f = Fernet(key)
            token = f.encrypt(bytes(f"{name}{time()}", encoding="utf-8"))
            data.write(f"{_id},{key},{token},100\n")


def generate_garbage_event():
    from datetime import datetime
    with open('./bookings/data/bookings.csv', 'w+') as data:
        data.write("roomId,userId,year,month,day,starttime,eventId,\n")

names = generate_random_rooms()
generate_random_public_private_keys(names)
generate_garbage_event()