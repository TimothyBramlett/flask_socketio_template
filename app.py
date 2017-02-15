from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import eventlet


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def index():
    return render_template('index.html')


@socketio.on('client_connected')
def test_message(message):
    #emit('my response', {'data': message['data']})
    print('my response', {'data': message['data']})

    upper_limit = 20
    x = 0
    while x < upper_limit:
        print(x)
        emit('number_counter_msg', x)
        eventlet.sleep(1)
        x += 1


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
