from time import sleep
import RPi.GPIO as GPIO
from flask_socketio import SocketIO

class Movement:
    """
    A class to control the movement of a stepper motor using GPIO pins and Flask-SocketIO.

    This class provides methods to move the motor to the left or right, start and stop continuous movement, and manage the current position of the motor.

    Attributes
    ----------
    step_pin : int
        The GPIO pin number for the step signal.
    direction_pin : int
        The GPIO pin number for the direction signal.
    enable_pin : int
        The GPIO pin number for the enable signal.
    socketio : SocketIO
        The SocketIO instance for emitting events.
    max_steps : int, optional
        The maximum number of steps the motor can take (default is 4050).
    us_delay : int, optional
        The delay between steps in microseconds (default is 950).
    pos : int
        The current position of the motor.
    steps : int
        The number of steps to move in one command.
    uS : float
        The conversion factor from microseconds to seconds.
    moving : bool
        The flag indicating whether the motor is currently moving.

    Methods
    -------
    set_step_length(steps):
        Sets the number of steps to move in one command.
    go_right(steps):
        Moves the motor to the right by the specified number of steps.
    go_left(steps):
        Moves the motor to the left by the specified number of steps.
    start_moving(direction):
        Starts continuous movement in the specified direction.
    stop_moving():
        Stops the continuous movement.
    _move_continuous(move_func):
        Continuously moves the motor using the specified movement function.
    get_current_pos():
        Returns the current position of the motor.
    set_current_pos(value):
        Sets the current position of the motor.
    """

    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int, socketio, max_steps=4050, us_delay=950):
        """
        Constructs all the necessary attributes for the Movement object.

        Parameters
        ----------
        step_pin : int
            The GPIO pin number for the step signal.
        direction_pin : int
            The GPIO pin number for the direction signal.
        enable_pin : int
            The GPIO pin number for the enable signal.
        socketio : SocketIO
            The SocketIO instance for emitting events.
        max_steps : int, optional
            The maximum number of steps the motor can take (default is 4050).
        us_delay : int, optional
            The delay between steps in microseconds (default is 950).
        """
        self.step_pin: int = step_pin
        self.direction_pin: int = direction_pin
        self.enable_pin: int = enable_pin
        self.pos: int = 0
        self.steps: int = 200
        self.us_delay: int = us_delay
        self.uS: float = 0.000001
        self.moving: bool = False
        self.max_steps: int = max_steps
        self.socketio = socketio

    def set_step_length(self, steps: int) -> None:
        """
        Sets the number of steps to move in one command.

        Parameters
        ----------
        steps : int
            The number of steps to move.
        """
        self.steps = steps

    def go_right(self, steps: int) -> None:
        """
        Moves the motor to the right by the specified number of steps.

        Parameters
        ----------
        steps : int
            The number of steps to move.
        """
        GPIO.output(self.direction_pin, GPIO.HIGH)
        for i in range(steps):
            if self.pos >= self.max_steps:
                print("Reached maximum steps")
                continue
            delay = self.uS * self.us_delay
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
            self.pos += 1
            self.socketio.emit('update_step_count', {'step_count': self.pos})
            print(f"Moving right: current position = {self.pos}")

    def go_left(self, steps: int) -> None:
        """
        Moves the motor to the left by the specified number of steps.

        Parameters
        ----------
        steps : int
            The number of steps to move.
        """
        GPIO.output(self.direction_pin, GPIO.LOW)
        for i in range(steps):
            if self.pos <= 0:
                print("Reached minimum steps")
                continue
            delay = self.uS * self.us_delay
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
            self.pos -= 1
            self.socketio.emit('update_step_count', {'step_count': self.pos})
            print(f"Moving left: current position = {self.pos}")

    def start_moving(self, direction: str) -> None:
        """
        Starts continuous movement in the specified direction.

        Parameters
        ----------
        direction : str
            The direction to move continuously ('left' or 'right').
        """
        self.moving = True
        if direction == 'left':
            self._move_continuous(self.go_left)
        elif direction == 'right':
            self._move_continuous(self.go_right)

    def stop_moving(self) -> None:
        """
        Stops the continuous movement.
        """
        self.moving = False

    def _move_continuous(self, move_func) -> None:
        """
        Continuously moves the motor using the specified movement function.

        Parameters
        ----------
        move_func : function
            The movement function to use for continuous movement.
        """
        while self.moving:
            move_func(1)

    def get_current_pos(self) -> int:
        """
        Returns the current position of the motor.

        Returns
        -------
        int
            The current position of the motor.
        """
        return self.pos

    def set_current_pos(self, value: int) -> None:
        """
        Sets the current position of the motor.

        Parameters
        ----------
        value : int
            The position to set.
        """
        self.pos = value
