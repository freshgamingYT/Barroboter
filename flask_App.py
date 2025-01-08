from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from servo import Servo
from config import ConfigManager
import threading

class FlaskApp:
    def __init__(self, config_file: str):
        self.config_manager = ConfigManager(config_file)
        self.config_file = 'config.json'

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = self.config_manager.get('secret_key')
        self.socketio = SocketIO(self.app)

        print("Initializing Servo in FlaskApp")
        self.servo = Servo(positions=self.config_manager.get('servo_steps'), 
                           step_pin=self.config_manager.get('step_pin'), 
                           direction_pin=self.config_manager.get('direction_pin'), 
                           enable_pin=self.config_manager.get('enable_pin'),
                           socketio=self.socketio,
                           velocity_settings=self.config_manager.get('velocity_settings'),
                           distance_thresholds=self.config_manager.get('distance_thresholds'),
                           config_file=self.config_file)

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', step_count=self.servo.movement.get_current_pos())

        @self.app.route('/current_position', methods=['GET'])
        def current_position():
            step_count = self.servo.movement.get_current_pos()
            return jsonify(step_count=step_count)

    def create_app(self):
        return self.app

    def cleanup(self) -> None:
        self.servo.cleanup()

def console_input(servo):
    while True:
        step = input("Enter step (pos1, pos2, ..., pos10) or 'exit' to quit: ")
        if step == 'exit':
            break
        servo.move_to(step)

if __name__ == '__main__':
    config_file = 'config.json'
    config = FlaskApp(config_file)    
    app = config.create_app()

    input_thread = threading.Thread(target=console_input, args=(config.servo,))
    input_thread.start()

    try:
        config.socketio.run(app, debug=True)
    finally:
        config.cleanup()
