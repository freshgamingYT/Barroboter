
from flask import Blueprint, render_template, request, jsonify
from flask_socketio import emit

class Views:
    """
    A class to set up routes and handle requests for the Flask application.

    Attributes
    ----------
    app : Flask
        The Flask application instance.
    servo : Servo
        The Servo instance for managing servo positions.
    servo_moves : ServoMoves
        The ServoMoves instance for controlling servo movements.
    socketio : SocketIO
        The SocketIO instance for real-time communication.

    Methods
    -------
    __init__(app, servo, servo_moves, socketio):
        Initializes the Views instance with the given Flask app, servo, servo_moves, and socketio.
    setup_routes():
        Sets up the routes for the Flask application.
    index():
        Renders the index page with the current step count.
    move():
        Handles the move request to start or stop servo movement.
    save_state():
        Handles the request to save the current state to a JSON file.
    load_state():
        Handles the request to load the state from a JSON file.
    """

    def __init__(self, app, servo, servo_moves, socketio):
        """
        Initializes the Views instance.

        Parameters
        ----------
        app : Flask
            The Flask application instance.
        servo : Servo
            The Servo instance for managing servo positions.
        servo_moves : ServoMoves
            The ServoMoves instance for controlling servo movements.
        socketio : SocketIO
            The SocketIO instance for real-time communication.
        """
        self.app = app
        self.servo = servo
        self.servo_moves = servo_moves
        self.socketio = socketio
        self.setup_routes()

    def setup_routes(self):
        """
        Sets up the routes for the Flask application.
        """
        @self.app.route('/')
        def index():
            """
            Renders the index page with the current step count.

            Returns
            -------
            str
                The rendered HTML of the index page.
            """
            return render_template('index.html', step_count=self.servo_moves.get_current_pos())

        @self.app.route('/move', methods=['POST'])
        def move():
            """
            Handles the move request to start or stop servo movement.

            Returns
            -------
            Response
                A JSON response with the current step count.
            """
            direction = request.json.get('direction')
            action = request.json.get('action')
            print(f"Received request: direction={direction}, action={action}")
            if action == 'start':
                self.servo_moves.start_moving(direction)
            elif action == 'stop':
                self.servo_moves.stop_moving()
            step_count = self.servo_moves.get_current_pos()
            self.socketio.emit('update_step_count', {'step_count': step_count})
            return jsonify(step_count=step_count)

        @self.app.route('/save_state', methods=['POST'])
        def save_state():
            """
            Handles the request to save the current state to a JSON file.

            Returns
            -------
            Response
                A JSON response indicating the success of the operation.
            """
            self.servo_moves.save_to_json('servo_state.json')
            return jsonify({"status": "success", "message": "State saved to servo_state.json"})

        @self.app.route('/load_state', methods=['POST'])
        def load_state():
            """
            Handles the request to load the state from a JSON file.

            Returns
            -------
            Response
                A JSON response with the current step count and a success message.
            """
            self.servo_moves.load_from_json('servo_state.json')
            step_count = self.servo_moves.get_current_pos()
            self.socketio.emit('update_step_count', {'step_count': step_count})
            return jsonify({"status": "success", "message": "State loaded from servo_state.json", "step_count": step_count})
