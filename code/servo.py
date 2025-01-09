import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0)

    def set_angle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        self.servo.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.pin, False)
        self.servo.ChangeDutyCycle(0)
