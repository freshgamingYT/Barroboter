
from gpio_setup import GPIOSetup
from movement import Movement
from config import ConfigManager

class ServoMoves:
    """
    A class to manage the movement and configuration of a servo motor.

    Attributes
    ----------
    gpio_setup : GPIOSetup
        An instance of the GPIOSetup class for setting up GPIO pins.
    movement : Movement
        An instance of the Movement class for controlling servo movements.
    config_manager : ConfigManager
        An instance of the ConfigManager class for saving and loading configurations.

    Methods
    -------
    __init__(step_pin, direction_pin, enable_pin, socketio):
        Initializes the ServoMoves instance with given GPIO pins and SocketIO instance.
    set_step_length(steps):
        Sets the step length for the servo movement.
    go_right(steps):
        Moves the servo to the right by the specified number of steps.
    go_left(steps):
        Moves the servo to the left by the specified number of steps.
    start_moving(direction):
        Starts continuous movement in the specified direction.
    stop_moving():
        Stops continuous movement.
    get_current_pos():
        Returns the current position of the servo.
    set_current_pos(value):
        Sets the current position of the servo.
    save_to_json(filename):
        Saves the current configuration to a JSON file.
    load_from_json(filename):
        Loads the configuration from a JSON file.
    cleanup():
        Cleans up the GPIO setup.
    """

    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int, socketio):
        """
        Initializes the ServoMoves instance.

        Parameters
        ----------
        step_pin : int
            The GPIO pin number for the step signal.
        direction_pin : int
            The GPIO pin number for the direction signal.
        enable_pin : int
            The GPIO pin number for the enable signal.
        socketio : SocketIO
            The SocketIO instance for real-time communication.
        """
        self.gpio_setup = GPIOSetup(step_pin, direction_pin, enable_pin)
        self.movement = Movement(step_pin, direction_pin, enable_pin, socketio)
        self.config_manager = ConfigManager(step_pin, direction_pin, enable_pin)

    def set_step_length(self, steps: int) -> None:
        """
        Sets the step length for the servo movement.

        Parameters
        ----------
        steps : int
            The number of steps for the servo movement.
        """
        self.movement.set_step_length(steps)

    def go_right(self, steps: int) -> None:
        """
        Moves the servo to the right by the specified number of steps.

        Parameters
        ----------
        steps : int
            The number of steps to move to the right.
        """
        self.movement.go_right(steps)

    def go_left(self, steps: int) -> None:
        """
        Moves the servo to the left by the specified number of steps.

        Parameters
        ----------
        steps : int
            The number of steps to move to the left.
        """
        self.movement.go_left(steps)

    def start_moving(self, direction: str) -> None:
        """
        Starts continuous movement in the specified direction.

        Parameters
        ----------
        direction : str
            The direction to move continuously ('left' or 'right').
        """
        self.movement.start_moving(direction)

    def stop_moving(self) -> None:
        """
        Stops continuous movement.
        """
        self.movement.stop_moving()

    def get_current_pos(self) -> int:
        """
        Returns the current position of the servo.

        Returns
        -------
        int
            The current position of the servo.
        """
        return self.movement.get_current_pos()

    def set_current_pos(self, value: int):
        """
        Sets the current position of the servo.

        Parameters
        ----------
        value : int
            The position to set for the servo.
        """
        self.movement.set_current_pos(value)

    def save_to_json(self, filename: str):
        """
        Saves the current configuration to a JSON file.

        Parameters
        ----------
        filename : str
            The path to the JSON file where the configuration will be saved.
        """
        self.config_manager.save_to_json(filename)

    def load_from_json(self, filename: str):
        """
        Loads the configuration from a JSON file.

        Parameters
        ----------
        filename : str
            The path to the JSON file from which the configuration will be loaded.
        """
        self.config_manager.load_from_json(filename)

    def cleanup(self) -> None:
        """
        Cleans up the GPIO setup.
        """
        self.gpio_setup.cleanup_gpio()
