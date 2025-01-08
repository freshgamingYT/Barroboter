from flask import render_template, request, jsonify

class Views:
    def __init__(self, app, servo, socketio):
        self.app = app
        self.servo = servo
        self.socketio = socketio
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', step_count=self.servo.movement.get_current_pos())

        @self.app.route('/current_position', methods=['GET'])
        def current_position():
            step_count = self.servo.movement.get_current_pos()
            return jsonify(step_count=step_count)
