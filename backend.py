from transitions import Machine
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import toml
import hashlib

PANIC_TIME = 60

app = Flask(__name__)
# необходимо чтобы не было проблем с CORS
cors = CORS(
    app,
    resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}},
)

class StorageCamera:
    def __init__(self):
        states = ["locked", "unlocked"]

        transitions = [
            {"trigger": "unlock", "source": "locked", "dest": "unlocked"},
            {"trigger": "lock", "source": "unlocked", "dest": "locked"},
        ]

        self.machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            initial="locked",
            auto_transitions=False,
        )

        self.door_opened = False
        self.panic = False

    def close_door(self):
        self.door_opened = False
        self.panic = False
        
    def open_door(self):
        self.door_opened = True
        self.start_monitoring()

    def monitor_door(self):
        time_passed = 0
        while self.door_opened:
            time.sleep(1)
            time_passed += 1
            if time_passed > PANIC_TIME:
                self.panic = True

    def start_monitoring(self):
        self.door_opened = True
        thread = threading.Thread(target=self.monitor_door)
        thread.start()


camera = StorageCamera()


@app.route("/", methods=["GET"])
def get_state():
    if camera.state == "locked":
        message = "Дверь закрыта. Введите пароль"
    elif camera.panic:
        message = "Срочно закройте дверь!"
    else:
        message = "Дверь открыта"
    return jsonify({"state": camera.state, "message": message})


@app.route("/unlock", methods=["POST"])
def unlock():
    if camera.state == "locked":
        data = request.get_json()
        config = toml.load("config/config.toml")
        hashed_pass = hashlib.sha256(data["password"]["password"].encode('UTF-8')).hexdigest()
        if hashed_pass == config['Door']['password']:
            camera.open_door()
            camera.unlock()
            message = "Дверь открыта"
        elif hashed_pass != config['Door']['password']:
            message = "Пароль неверный"
    else:
        message = "Дверь уже открыта"
    return jsonify({"state": camera.state, "message": message})


@app.route("/lock", methods=["POST"])
def lock():
    if camera.state == "unlocked":
        camera.close_door()
        camera.lock()
        message = "Дверь закрыта. Введите пароль"
    else:
        message = "Дверь уже закрыта"
    return jsonify({"state": camera.state, "message": message})

if __name__ == "__main__":
    app.run(debug=True)
