import RPi.GPIO as GPIO

"""
A class to set up and manage GPIO pins for a stepper motor.

This class provides methods to initialize and clean up GPIO pins used for controlling a stepper motor. It sets up the pins for step, direction, and enable signals.

Attributes
----------
step_pin : int
    The GPIO pin number for the step signal.
direction_pin : int
    The GPIO pin number for the direction signal.
enable_pin : int
    The GPIO pin number for the enable signal.

Methods
-------
setup_gpio():
    Sets up the GPIO pins and initializes the enable pin to LOW.
cleanup_gpio():
    Cleans up the GPIO settings.
"""

class GPIOSetup:
    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int):
        """
        Constructs all the necessary attributes for the GPIOSetup object.

        Parameters
        ----------
        step_pin : int
            The GPIO pin number for the step signal.
        direction_pin : int
            The GPIO pin number for the direction signal.
        enable_pin : int
            The GPIO pin number for the enable signal.
        """
        self.step_pin: int = step_pin
        self.direction_pin: int = direction_pin
        self.enable_pin: int = enable_pin
        self.setup_gpio()

    def setup_gpio(self) -> None:
        """
        Sets up the GPIO pins and initializes the enable pin to LOW.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)

    def cleanup_gpio(self) -> None:
        """
        Cleans up the GPIO settings.
        """
        GPIO.cleanup()
