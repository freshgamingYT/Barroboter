from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

move_low_route = Blueprint('move_low_route', __name__)

@move_low_route.route('/move-low', methods=['POST'])
def move_low():
    data = request.get_json()
    logger.debug(f'Received move_low command: {data}')
    # Add your move_low logic here
    return jsonify({'status': 'success'})
