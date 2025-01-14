from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

move_mid_route = Blueprint('move_mid_route', __name__)

@move_mid_route.route('/move-mid', methods=['POST'])
def move_mid():
    data = request.get_json()
    logger.debug(f'Received move_mid command: {data}')
    # Add your move_mid logic here
    return jsonify({'status': 'success'})
