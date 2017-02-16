from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import eventlet
import logging
import platform
import os

# Needed if you only want to start the thead once
thread = None

# For logging
if platform.platform().startswith('Windows'):
    logging_file = os.path.dirname(os.path.realpath(__file__)) + r'\test.log'
logging.basicConfig(filename=logging_file, level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# specifically sets eventlet rather than letting the library choose
socketio = SocketIO(app, async_mode='eventlet')


def background_thread(room_name):
    """Streams data to the client in real time using websockets"""
    count = 0
    while count < 100:
        socketio.sleep(1)
        count += 1
        print(count)
        socketio.emit('number_counter_msg',
                      count,
                      namespace='/counter', room=room_name)

# This is a traditional flask route to deliver the client js code and web page
@app.route('/', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

# Websocket view that launches a background thread when client notifies the server
# that it has connected
@socketio.on('client_connected', namespace='/counter')
def start_counter(message):
    room_name = request.sid
    thread = socketio.start_background_task(target=background_thread, room_name=room_name)
    emit('number_counter_msg', 'Thread Started...')


## This is the same as the above but it does not create a new bg thread
## if one already exists.  Keeping this around for now.
# @socketio.on('client_connected', namespace='/counter')
# def start_counter(message):
#     global thread
#     if thread is None:
#         thread = socketio.start_background_task(target=background_thread)
#     else:
#         print('Thread already started.')
#     emit('number_counter_msg', 'Thread Started...')

## This is the version I was using before but has the issue of emit() not sending
## Any data until the loop is finished.
# @socketio.on('client_connected', namespace='/counter')
# def test_message(message):
#     #emit('my response', {'data': message['data']})
#     print('my response', {'data': message['data']})
#
#     upper_limit = 10
#     x = 0
#     while x < upper_limit:
#         print('{} - {}'.format(x, request.sid))
#         emit('number_counter_msg', x, namespace='/counter')
#         eventlet.greenthread.sleep(2)
#         x += 1


@socketio.on('connect')
def test_connect():
    print('Server Detected Connection from Client.')



if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=False)