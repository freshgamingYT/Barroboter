from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger('my_logger')

select_cocktails_route = Blueprint('select_cocktails_route', __name__)

@select_cocktails_route.route('/select-cocktail', methods=['POST'])
def select():
    data = request.get_json()
    logger.debug(f'Received select button press: {data}')
    if data['button'] == 'start':
        # Execute the sequence of movements
        movement = Movement(
            positions_file='../json/positions.json',
            sequence_file='../json/sequence.json',
            config_file='../json/config.json'
        )
        movement.initialize_stepper()
        movement.execute_sequence()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'})

def register_select_routes(app):
    app.register_blueprint(select_cocktails_route, url_prefix="/api")
    logger.debug('Select routes registered successfully')
