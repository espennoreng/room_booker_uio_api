from datetime import datetime, timedelta
import time
import schedule
from flask import Flask, request, jsonify
from app.roomBooker import RoomBooker
from flask_cors import CORS, cross_origin
from app.decrypt import Decrypt
from threading import Thread


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

room = RoomBooker()

# create a thread to run the scheduler





@app.route('/get-rooms', methods=['POST'])
@cross_origin()
def get_available_rooms(room=room):
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        try:
            password = data['password']
            username = data['username']
            building = data['building']
            date_time = data['date']
            duration = data['duration']

            # hei
            date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            year, month, day = date_time.year, date_time.month, date_time.day
            month = datetime.strptime(str(month), "%m").strftime("%B")
            start_time = date_time.strftime('%H:%M')
            end_time = (date_time + timedelta(hours=duration)
                        ).strftime('%H:%M')

            # if roomboker does not exist create one,
            if room.is_logged_in() is False:
                d = Decrypt()
                password = d.decrypt(password)
                username = d.decrypt(username)
                room.login(password, username)

            available_rooms = room.get_available_rooms(
                building, year, month, day, start_time, end_time)

            return jsonify(available_rooms)

        except Exception as e:
            print(e)
            return jsonify({'message': 'Missing key in request', 'error': str(e)}), 400


@app.route('/book', methods=['POST'])
@cross_origin()
def book_room():
    if request.method == "POST":
        data = request.get_json()

        try:
            building = data['building']
            date_time = data['date']
            duration = data['duration']
            room = data['room']
            attendees = data['attendees']
            text = data['text']
            title = data['title']
            password = data['password']
            username = data['username']

            date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            year, month, day = date_time.year, date_time.month, date_time.day
            month = datetime.strptime(str(month), "%m").strftime("%B")
            start_time = date_time.strftime('%H:%M')
            end_time = (date_time + timedelta(hours=duration)
                        ).strftime('%H:%M')

            room_booker = RoomBooker(username, password)
            try:
                book_room = room_booker.book(
                    building, room, year, month, day, start_time, end_time, title, text, attendees)
                if book_room:
                    print("room booked")
                else:
                    print('Room not booked')
            except Exception as e:
                print(e)
                return jsonify({'message': 'Error booking room', 'error': str(e)}), 400

            if book_room:
                return jsonify({
                    'status': 'success',
                    'info': {
                        'building': building,
                        'room': room,
                        'start_time': start_time,
                        'end_time': end_time,
                        'date': date_time,
                        'duration': duration,
                        'attendees': attendees,
                        'text': text
                    }
                }), 200
            else:
                return jsonify({'status': 'failed'}), 400

        except Exception as e:
            return jsonify({'message': 'Missing key in request', "error": str(e)}), 400


@app.route('/update-rooms', methods=['POST'])
@cross_origin()
def update_rooms():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        try:
            password = data['password']
            username = data['username']

            if room.is_logged_in() is False:
                d = Decrypt()
                password = d.decrypt(password)
                username = d.decrypt(username)
                room.login(password, username)

            room.update_availability()

            return jsonify({'status': 'success'}), 200

        except Exception as e:
            return jsonify({'message': 'Missing key in request', 'error': str(e)}), 400


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to the uio_room_book_api!</h1>"


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
