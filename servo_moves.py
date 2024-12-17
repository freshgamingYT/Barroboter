from time import sleep
import math
import RPi.GPIO as GPIO



class Servo_moves:
    
    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

        self.pos: int = 0   # initial starting pos
        self.steps: int = 200  # number of steps
        self.usDelay: int = 950  # number of microseconds 
        self.uS: float = 0.000001  # one microsecond

        GPIO.output(self.enable_pin, GPIO.LOW)

    def set_step_length(self, steps: int) -> None:
        self.steps = steps

    def goRight(self, steps: int) -> None:
        print('2')
        GPIO.output(self.direction_pin, GPIO.HIGH)  # Set direction to right
        for i in range(steps):
            progress = i / steps

            #sinus
            delay_factor = 0.5 * (1 - math.cos(math.pi * progress))
            delay = self.uS * self.usDelay * delay_factor

            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
            
    def goLeft(self, steps: int) -> None:
        GPIO.output(self.direction_pin, GPIO.LOW)  # Set direction to right
        for i in range(steps):
            progress = i / steps

            #sinus
            delay_factor = 0.5 * (1 - math.cos(math.pi * progress))
            delay = self.uS * self.usDelay * delay_factor

            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)

    def get_current_pos(self) -> int:
        return self.pos   
    
    def set_current_pos(self, value: int) -> None:
        self.pos = value
