from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from servo_moves import ServoMoves
from servo import Servo
import views
import json

class FlaskApp:
    """
    A class to represent the Flask application with SocketIO support.

    Attributes
    ----------
    app : Flask
        The Flask application instance.
    socketio : SocketIO
        The SocketIO instance for real-time communication.
    servo_move : ServoMoves
        The ServoMoves instance for controlling servo movements.
    servo : Servo
        The Servo instance for managing servo positions.
    views : Views
        The Views instance for setting up routes.

    Methods
    -------
    __init__():
        Initializes the FlaskApp instance, loads configuration, and sets up components.
    load_config(filename: str) -> None:
        Loads configuration from a JSON file.
    create_app():
        Returns the Flask application instance.
    cleanup() -> None:
        Cleans up resources.
    """

    def __init__(self):
        """
        Initializes the FlaskApp instance.

        Sets up the Flask application, loads configuration, initializes
        ServoMoves and Servo instances, and sets up routes.
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'Keins123!'
        self.socketio = SocketIO(self.app)

        # Load configuration from JSON file
        self.load_config('config.json')

        print("Initializing ServoMoves in FlaskApp")
        self.servo_move = ServoMoves(step_pin=self.config['step_pin'], 
                                     direction_pin=self.config['direction_pin'], 
                                     enable_pin=self.config['enable_pin'],
                                     socketio=self.socketio)
        
        print("Initializing Servo in FlaskApp")
        self.servo = Servo(positions=self.config['servo_steps'], 
                           step_pin=self.config['step_pin'], 
                           direction_pin=self.config['direction_pin'], 
                           enable_pin=self.config['enable_pin'],
                           socketio=self.socketio)
        
        self.views = views.Views(self.app, self.servo, self.servo_move, self.socketio)
    
    def load_config(self, filename: str) -> None:
        """
        Loads configuration from a JSON file.

        Parameters
        ----------
        filename : str
            The path to the JSON configuration file.
        """
        with open(filename, 'r') as f:
            self.config = json.load(f)

    def create_app(self):
        """
        Returns the Flask application instance.

        Returns
        -------
        Flask
            The Flask application instance.
        """
        return self.app

    def cleanup(self) -> None:
        """
        Cleans up resources by calling the cleanup method of ServoMoves.
        """
        self.servo_move.cleanup()

if __name__ == '__main__':
    config = FlaskApp()
    app = config.create_app()
    try:
        config.socketio.run(app, debug=True)
    finally:
        config.cleanup()
