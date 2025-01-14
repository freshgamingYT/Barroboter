from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

move_route = Blueprint('move_route', __name__)

@move_route.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    logger.debug(f'Received move command: {data}')
    # Add your move logic here
    return jsonify({'status': 'success'})
