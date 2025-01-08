from time import sleep
import RPi.GPIO as GPIO

class Movement:
    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int, left_button_pin: int, right_button_pin: int, socketio, velocity_settings: dict, max_steps=4050):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin
        self.left_button_pin = left_button_pin
        self.right_button_pin = right_button_pin
        self.pos = 0
        self.steps = 200
        self.us_delay = 950
        self.uS = 0.000001
        self.moving = False
        self.max_steps = max_steps
        self.socketio = socketio
        self.velocity = 0
        self.velocity_settings = velocity_settings
        self.initialized = False

        # Set GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.left_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.enable_pin, GPIO.LOW)

    def set_step_length(self, steps: int) -> None:
        self.steps = steps

    def set_velocity(self, velocity: int) -> None:
        self.velocity = velocity
        if velocity == 0:
            self.us_delay = float('inf')  # Stop movement
        elif velocity == 1:
            self.us_delay = self.velocity_settings['velocity_1']
        elif velocity == 2:
            self.us_delay = self.velocity_settings['velocity_2']
        elif velocity == 3:
            self.us_delay = self.velocity_settings['velocity_3']

    def move_to_position(self, target_pos: int) -> None:
        current_pos = self.pos
        if target_pos > current_pos:
            self.accelerate()
            self.move_right(target_pos - current_pos)
            self.decelerate()
        elif target_pos < current_pos:
            self.accelerate()
            self.move_left(current_pos - target_pos)
            self.decelerate()

    def accelerate(self) -> None:
        for v in range(1, self.velocity + 1):
            self.set_velocity(v)
            sleep(0.5)  # Adjust the sleep time as needed for smoother acceleration

    def decelerate(self) -> None:
        for v in range(self.velocity, 0, -1):
            self.set_velocity(v)
            sleep(0.5)  # Adjust the sleep time as needed for smoother deceleration

    def move_right(self, steps: int) -> None:
        GPIO.output(self.direction_pin, GPIO.HIGH)
        for i in range(steps):
            if self.pos >= self.max_steps or GPIO.input(self.right_button_pin) == GPIO.LOW:
                print("Reached maximum steps or right button pressed")
                break
            delay = self.uS * self.us_delay
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
            self.pos += 1
            self.socketio.emit('update_step_count', {'step_count': self.pos})
            print(f"Moving right: current position = {self.pos}")

    def move_left(self, steps: int) -> None:
        GPIO.output(self.direction_pin, GPIO.LOW)
        for i in range(steps):
            if self.pos <= 0 or GPIO.input(self.left_button_pin) == GPIO.LOW:
                print("Reached minimum steps or left button pressed")
                break
            delay = self.uS * self.us_delay
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
            self.pos -= 1
            self.socketio.emit('update_step_count', {'step_count': self.pos})
            print(f"Moving left: current position = {self.pos}")

    def move_to_left_button(self) -> None:
        if not self.initialized:
            GPIO.output(self.direction_pin, GPIO.LOW)
            print("Moving to left button")
            while GPIO.input(self.left_button_pin) == GPIO.HIGH:
                delay = self.uS * self.us_delay
                GPIO.output(self.step_pin, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                sleep(delay)
                self.pos -= 1
                self.socketio.emit('update_step_count', {'step_count': self.pos})
                print(f"Moving left to button: current position = {self.pos}")
            self.set_current_pos(0)
            self.initialized = True
            print("Left button pressed, position set to 0")

    def get_current_pos(self) -> int:
        return self.pos

    def set_current_pos(self, value: int) -> None:
        self.pos = value

    def cleanup(self):
        GPIO.cleanup()
