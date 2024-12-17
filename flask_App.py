from flask import Flask, render_template, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
from servo import Servo
from servo_moves import Servo_moves
from Views import Views

class AppConfig:
    servo_steps = {
        "pos1": 0,
        "pos2": 450,
        "pos3": 900,
        "pos4": 1350,
        "pos5": 1800,
        "pos6": 2250,
        "pos7": 2700,
        "pos8": 3150,
        "pos9": 3600,
        "pos10": 4050
    }
    
    step_pin = 17         # step pin
    direction_pin = 18    # direction pin
    enable_pin = 27       # enable pin

    def __init__(self):
        #self.db = SQLAlchemy()
        #DB_NAME = 'ServoStep.db'
        
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'Keins123!'
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
        self.db.init_app(self.app)

        self.servo_moves = Servo_moves(step_pin=self.step_pin, 
                                     direction_pin=self.direction_pin, 
                                     enable_pin=self.enable_pin)
        self.servo = Servo(self.servo_steps, self.servo_moves)
        self.views = Views(self.app, self.servo, self.servo_moves)
    
    def create_app(self):
        return self.app

if __name__ == '__main__':
    config = AppConfig()
    app = config.create_app()
    app.run(debug=True)