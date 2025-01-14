from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

stepper_init_route = Blueprint('stepper_init_route', __name__)

@stepper_init_route.route('/init', methods=['POST'])
def stepper_init():
    data = request.get_json()
    logger.debug(f'Received stepper_init command: {data}')
    # Add your stepper_init logic here
    return jsonify({'status': 'success'})
