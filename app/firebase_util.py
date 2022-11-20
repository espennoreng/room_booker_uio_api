import firebase_admin
from firebase_admin import firestore, credentials
from app.data import get_all_uio_rooms


# connect to firestore
cred = credentials.Certificate('app/sa.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'rooms').document(u'available_rooms')

# set collection name
collection_name = 'rooms'

# set document name
document_name = 'available_rooms'


def set_available_rooms(available_rooms):

    # set document name
    collection_name = 'rooms'

    for room in available_rooms:
        room_new = room.replace('(', '').replace(
            ')', '').replace(':', '').strip().split(' ')
        building = room_new[0]
        room_name = room_new[1] + ' ' + room_new[2]
        room_id = room_new[3]

        doc_ref = db.collection(collection_name).document(
            room_name + ' ' + room_id)
        data = {
            "available": True,
            "building": building,
            "room_name": room_name,
            "room_id": room_id,
            "full_name": room,
            "last_updated": firestore.SERVER_TIMESTAMP
        }
        doc_ref.set(data, merge=True)

    print('done setting available rooms')


def update_available_rooms(available_rooms, duration: int, last_room_and_duration: dict):

    all_ojd_rooms = get_all_uio_rooms()['OJD']

    for room in available_rooms:
        room_new = room.replace('(', '').replace(
            ')', '').replace(':', '').strip().split(' ')
        room_name = room_new[1] + ' ' + room_new[2]
        room_id = room_new[3]

        doc_ref = db.collection(collection_name).document(
            room_name + ' ' + room_id)
        data = {
            "available": True,
            "last_updated": firestore.SERVER_TIMESTAMP,
        }
        if (room in last_room_and_duration.keys()):
            # if duration is bigger than the one in firestore
            if duration > last_room_and_duration[room] or len(last_room_and_duration) == 0:
                data['available_duration'] = duration

                doc_ref.update(data)

    for room in all_ojd_rooms:
        if room not in available_rooms:
            room_new = room.replace('(', '').replace(
                ')', '').replace(':', '').strip().split(' ')
            room_name = room_new[1] + ' ' + room_new[2]
            room_id = room_new[3]

            doc_ref = db.collection(collection_name).document(
                room_name + ' ' + room_id)
            data = {
                "available": False,
                "last_updated": firestore.SERVER_TIMESTAMP,
                "available_duration": 0
            }
            if len(last_room_and_duration) == 0:
                doc_ref.update(data)

    print('done updating available rooms')
