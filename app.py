from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import eventlet
import logging
import platform
import os

thread = None

if platform.platform().startswith('Windows'):
    logging_file = os.path.dirname(os.path.realpath(__file__)) + r'\test.log'

logging.basicConfig(filename=logging_file, level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while count < 100:
        socketio.sleep(1)
        count += 1
        print(count)
        socketio.emit('number_counter_msg',
                      count,
                      namespace='/counter')


@app.route('/', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def index():
    return render_template('index.html')




@socketio.on('client_connected', namespace='/counter')
def start_counter(message):

    thread = socketio.start_background_task(target=background_thread)
    emit('number_counter_msg', 'Thread Started...')



# # old version
# @socketio.on('client_connected', namespace='/counter')
# def start_counter(message):
#     global thread
#     if thread is None:
#         thread = socketio.start_background_task(target=background_thread)
#     else:
#         print('Thread already started.')
#     emit('number_counter_msg', 'Thread Started...')



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


# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)
#
@socketio.on('connect')
def test_connect():
    # emit('my response', {'data': 'Connected'})
    print('Server Detected Connection from Client.')
#
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')



if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=False)
