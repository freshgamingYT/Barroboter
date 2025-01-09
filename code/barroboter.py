import json
import RPi.GPIO as GPIO
import time
from config import Config
from servo import Servo
from stepper_moter import StepperMotor

class Barroboter:
    def __init__(self, config):
        self.config = config
        self.servo = Servo(config.data['servo_pin'])
        self.stepper = StepperMotor(config.data['stepper_pins'], config.data['step_delay'])

    def load_positions(self, path):
        with open(path) as positions_file:
            self.positions = json.load(positions_file)

    def load_ingredients(self, path):
        with open(path) as ingredients_file:
            self.ingredients = json.load(ingredients_file)

    def start(self):
        self.servo.set_angle(0)
        while GPIO.input(self.config.data['initial_position_button_pin']) == GPIO.HIGH:
            self.stepper.move(1, self.config.data['stepper_direction_left'])

        for ingredient in self.ingredients:
            position = self.positions[ingredient['position']]
            self.stepper.move(position['steps'], position['direction'])
            time.sleep(self.config.data['flow_rate_delay'])

        while GPIO.input(self.config.data['final_position_button_pin']) == GPIO.HIGH:
            self.stepper.move(1, self.config.data['stepper_direction_right'])
