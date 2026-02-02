from flask import Flask, render_template
from flask_socketio import SocketIO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

VALID = {"MAJU", "MUNDUR", "STOP"}
last_data = None

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("video")
def handle_video(data):
    socketio.emit("video", data)

@socketio.on("control")
def handle_control(data):
    global last_data

    # Format: LEFT:MAJU;RIGHT:MUNDUR
    try:
        left, right = data.split(";")
        _, lval = left.split(":")
        _, rval = right.split(":")
    except:
        logging.warning(f"Format salah: {data}")
        return

    if lval not in VALID or rval not in VALID:
        logging.warning(f"Data tidak valid: {data}")
        return

    if data != last_data:
        logging.info(f"LEFT={lval} | RIGHT={rval}")
        last_data = data

    socketio.emit("control", data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
