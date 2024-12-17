
from servo_moves import ServoMoves

class Servo:
    """
    A class to represent a servo motor and manage its movements.

    Attributes
    ----------
    servo_move : ServoMoves
        An instance of the ServoMoves class to control the servo motor.
    positions : dict
        A dictionary mapping step names to their corresponding positions.

    Methods
    -------
    __init__(positions: dict, step_pin: int, direction_pin: int, enable_pin: int, socketio):
        Initializes the Servo instance with given positions, GPIO pins, and SocketIO instance.
    move_to(step: str) -> None:
        Moves the servo to the specified step position.
    set_step_length(steps: int) -> None:
        Sets the step length for the servo movement.
    """

    def __init__(self, positions: dict, step_pin: int, direction_pin: int, enable_pin: int, socketio):
        """
        Initializes the Servo instance.

        Parameters
        ----------
        positions : dict
            A dictionary mapping step names to their corresponding positions.
        step_pin : int
            The GPIO pin number for the step signal.
        direction_pin : int
            The GPIO pin number for the direction signal.
        enable_pin : int
            The GPIO pin number for the enable signal.
        socketio : SocketIO
            The SocketIO instance for real-time communication.
        """
        self.servo_move = ServoMoves(step_pin=step_pin, direction_pin=direction_pin, enable_pin=enable_pin, socketio=socketio)
        self.positions: dict = positions

    def move_to(self, step: str) -> None:
        """
        Moves the servo to the specified step position.

        Parameters
        ----------
        step : str
            The name of the step to move to.
        """
        if step in self.positions:
            target_pos = self.positions[step]
            current_pos = self.servo_move.get_current_pos()

            if target_pos < current_pos:
                steps = current_pos - target_pos
                self.servo_move.go_left(steps)  # Corrected method call

            elif target_pos > current_pos:
                steps = target_pos - current_pos
                self.servo_move.go_right(steps)  # Corrected method call

            self.servo_move.set_current_pos(target_pos)
        else:
            print(f"Step {step} not found")

    def set_step_length(self, steps: int) -> None:
        """"
        
        Sets the step length for the servo movement.

        Parameters
        ----------
        steps : int
            The number of steps for the servo movement.
        """
        self.servo_move.set_step_length(steps)
