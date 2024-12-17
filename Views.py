from flask import Blueprint, render_template, request, jsonify

class Views:
    def __init__(self, app, servo_moves):
        self.app = app
        self.servo_moves = servo_moves
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', step_count=self.servo_moves.get_current_pos())

        @self.app.route('/move', methods=['POST'])
        def move():
            direction = request.json.get('direction')
            action = request.json.get('action')
            if action == 'start':
                self.servo_moves.start_moving(direction)
            elif action == 'stop':
                self.servo_moves.stop_moving()
            return jsonify(step_count=self.servo_moves.get_current_pos())
