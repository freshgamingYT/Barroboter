import RPi.GPIO as GPIO
from time import sleep

class Servo_moves:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    pos: int = 0   # initial starting pos
    steps: int = 200  # number of steps
    usDelay: int = 950  # number of microseconds 
    uS: float = 0.000001  # one microsecond
    moving: bool = False

    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin

        print(f"Initializing GPIO: step_pin={self.step_pin}, direction_pin={self.direction_pin}, enable_pin={self.enable_pin}")
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)

    def set_step_length(self, steps: int) -> None:
        self.steps = steps

    def goRight(self, steps: int) -> None:
        GPIO.output(self.direction_pin, GPIO.HIGH)  # Set direction to right
        for i in range(steps):
            delay = self.uS * self.usDelay

            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
            
    def goLeft(self, steps: int) -> None:
        GPIO.output(self.direction_pin, GPIO.LOW)  # Set direction to left
        for i in range(steps):
            delay = self.uS * self.usDelay

            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)

    def get_current_pos(self) -> int:
        return self.pos   
    
    def set_current_pos(self, value: int) -> None:
        self.pos = value

    def start_moving(self, direction: str) -> None:
        self.moving = True
        if direction == 'left':
            self._move_continuous(self.goLeft)
        elif direction == 'right':
            self._move_continuous(self.goRight)

    def stop_moving(self) -> None:
        self.moving = False

    def _move_continuous(self, move_func) -> None:
        while self.moving:
            move_func(1)  # Move one step at a time

    def cleanup(self) -> None:
        GPIO.cleanup()
