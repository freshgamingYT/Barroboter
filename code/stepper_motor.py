import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, pins, step_delay):
        self.pins = pins
        self.step_delay = step_delay
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def move(self, steps, direction):
        for _ in range(steps):
            for pin in self.pins:
                GPIO.output(pin, direction)
            time.sleep(self.step_delay)
