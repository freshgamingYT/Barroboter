from flask import Flask, render_template, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
import servo
import servo_moves
# from views import Views
import views

class Flask_App:
    servo_steps: dict = {
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
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'Keins123!'

        self.servo_moves = servo_moves.Servo_moves(step_pin=self.step_pin, 
                                     direction_pin=self.direction_pin, 
                                     enable_pin=self.enable_pin)
        
        self.servo = servo.Servo(self.servo_steps, 
                           step_pin=self.step_pin, 
                           direction_pin=self.direction_pin, 
                           enable_pin=self.enable_pin)
        self.views = views.Views(self.app, self.servo, self.servo_moves)
    
    def create_app(self):
        return self.app

if __name__ == '__main__':
    config = Flask_App()
    app = config.create_app()
    app.run(debug=True)
