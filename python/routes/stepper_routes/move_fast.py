from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

move_fast_route = Blueprint('move_fast_route', __name__)

@move_fast_route.route('/move-fast', methods=['POST'])
def move_fast():
    data = request.get_json()
    logger.debug(f'Received move_fast command: {data}')
    # Add your move_fast logic here
    return jsonify({'status': 'success'})
