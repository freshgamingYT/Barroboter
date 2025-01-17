from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from StepperInit import StepperInit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the stepper motor
stepper = StepperInit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cocktail/<int:id>')
def cocktail(id):
    return render_template(f'C{id}.html')

@app.route('/api/select-cocktail', methods=['POST'])
def select_cocktail():
    data = request.json
    cocktail_name = data.get('cocktail_name')
    if cocktail_name in stepper.available_cocktails:
        sequence_file = f"./json/sequences/{cocktail_name}_sequence.json"
        if os.path.exists(sequence_file):
            sequence_file_handler = FileHandler(sequence_file)
            sequence = sequence_file_handler.readJson()
            stepper.execute_sequence(sequence)
            return jsonify({"status": "success", "message": f"{cocktail_name} is being prepared."})
        else:
            return jsonify({"status": "error", "message": f"{cocktail_name}_sequence.json file not found."})
    else:
        return jsonify({"status": "error", "message": "Invalid cocktail name."})

@app.route('/api/stepper/status', methods=['GET'])
def stepper_status():
    status = {
        "current_position": stepper.aktuellePos,
        "is_moving": stepper.is_moving,
        "direction": stepper.direction,
        "limit_switch_status": {
            "left": stepper.getSchalterLinksStatus(),
            "right": stepper.getSchalterRechtsStatus()
        }
    }
    return jsonify(status)

@app.route('/api/stepper/move-fast', methods=['POST'])
def move_fast():
    data = request.json
    target_position = data.get('target_position')
    stepper.move_to_position(target_position, speed='fast')
    return jsonify({"status": "success", "message": "Stepper moved to position quickly."})

@app.route('/api/stepper/move-mid', methods=['POST'])
def move_mid():
    data = request.json
    target_position = data.get('target_position')
    stepper.move_to_position(target_position, speed='mid')
    return jsonify({"status": "success", "message": "Stepper moved to position at medium speed."})

@app.route('/api/stepper/move-slow', methods=['POST'])
def move_slow():
    data = request.json
    target_position = data.get('target_position')
    stepper.move_to_position(target_position, speed='slow')
    return jsonify({"status": "success", "message": "Stepper moved to position slowly."})

@app.route('/api/stepper/init', methods=['POST'])
def init_stepper():
    stepper.init()
    return jsonify({"status": "success", "message": "Stepper initialized."})

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
