from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from server.song_handler import Queue


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

sio = SocketIO(app)

thread = None

@app.route('/')
def index():
    global thread

    if thread is None:
        thread = sio.start_background_task(target=queue.run)

    return render_template("index.html")


@sio.on('connect')
def connection_handler():
    print("Connected: {}".format(request.sid))

    emit('update', queue.get_update_data())


@sio.on('disconnect')
def disconnection_handler():
    print("Disconnected: {}".format(request.sid))


@sio.on('submit')
def submit_song(song):
    try:
        queue.add(song)
    except Exception:
        pass


@sio.on('skip')
def skip():
    queue.next()


@sio.on('volume')
def set_volume(volume):
    queue.set_volume(volume)

queue = Queue(sio)


if __name__ == '__main__':
    sio.run(app, host="0.0.0.0")
