from flask import Flask
from flask_socketio import SocketIO
from servo import Servo
from config import ConfigManager
import views
import threading
import signal
import sys

class FlaskApp:
    def __init__(self, config_file: str):
        self.config_manager = ConfigManager(config_file)
        self.config_file = config_file

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = self.config_manager.get('secret_key')
        self.socketio = SocketIO(self.app)

        print("Initializing Servo in FlaskApp")
        self.servo = Servo(positions=self.config_manager.get('servo_steps'), 
                           step_pin=self.config_manager.get('step_pin'), 
                           direction_pin=self.config_manager.get('direction_pin'), 
                           enable_pin=self.config_manager.get('enable_pin'),
                           left_button_pin=self.config_manager.get('left_button_pin'),
                           right_button_pin=self.config_manager.get('right_button_pin'),
                           socketio=self.socketio,
                           velocity_settings=self.config_manager.get('velocity_settings'),
                           distance_thresholds=self.config_manager.get('distance_thresholds'))

        self.views = views.Views(self.app, self.servo, self.socketio)

        # Register signal handler for SIGINT
        signal.signal(signal.SIGINT, self.signal_handler)

        # Initialize the threading event to manage the console input thread
        self.stop_event = threading.Event()

    def create_app(self):
        return self.app

    def cleanup(self) -> None:
        print("Cleaning up GPIO")
        self.servo.cleanup()
        self.stop_event.set()

    def signal_handler(self, sig, frame):
        print("SIGINT received, cleaning up...")
        self.cleanup()
        sys.exit(0)

    def console_input(self):
        possible_steps = ", ".join(self.servo.positions.keys())
        print(f"Enter step ({possible_steps}) or 'exit' to quit:")
        while not self.stop_event.is_set():
            step = input()
            if step == 'exit':
                self.cleanup()
                sys.exit(0)
            if step in self.servo.positions:
                self.servo.move_to(step)
            else:
                print(f"Invalid step. Please enter one of the following: {possible_steps}")

if __name__ == '__main__':
    config_file = 'config.json'
    config = FlaskApp(config_file)    
    app = config.create_app()

    # Initialize the servo position
    config.servo.initialize_position()

    input_thread = threading.Thread(target=config.console_input)
    input_thread.start()

    try:
        config.socketio.run(app, debug=True)
    finally:
        config.cleanup()
        input_thread.join()
