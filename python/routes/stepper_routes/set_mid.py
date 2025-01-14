from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

set_mid_route = Blueprint('set_mid_route', __name__)

@set_mid_route.route('/set-mid', methods=['POST'])
def set_mid():
    data = request.get_json()
    logger.debug(f'Received set_mid command: {data}')
    return jsonify({'status': 'success'})

