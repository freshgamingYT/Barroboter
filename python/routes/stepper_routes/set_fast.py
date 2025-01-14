from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

set_fast_route = Blueprint('set_fast_route', __name__)

@set_fast_route.route('/set-fast', methods=['POST'])
def set_fast():
    data = request.get_json()
    logger.debug(f'Received set_fast command: {data}')
    # Add your set_fast logic here
    return jsonify({'status': 'success'})
