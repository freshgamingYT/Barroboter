from .move_fast import move_fast_route
from .move_mid import move_mid_route
from .move_low import move_low_route
from .move import move_route
from .set_fast import set_fast_route
from .set_mid import set_mid_route
from .set_low import set_low_route
from .status import status_route
from .stepper_init import stepper_init_route

def register_stepper_routes(app):
    app.register_blueprint(move_fast_route, url_prefix="/api/stepper")
    app.register_blueprint(move_mid_route, url_prefix="/api/stepper")
    app.register_blueprint(move_low_route, url_prefix="/api/stepper")
    app.register_blueprint(move_route, url_prefix="/api/stepper")
    app.register_blueprint(set_fast_route, url_prefix="/api/stepper")
    app.register_blueprint(set_mid_route, url_prefix="/api/stepper")
    app.register_blueprint(set_low_route, url_prefix="/api/stepper")
    app.register_blueprint(status_route, url_prefix="/api/stepper")
    app.register_blueprint(stepper_init_route, url_prefix="/api/stepper")
    logger.debug('Stepper routes registered successfully')
