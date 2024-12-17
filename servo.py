import servo_moves

class Servo:
    
    def __init__(self, positions: dict, step_pin: int, direction_pin: int, enable_pin: int):
        self.servo_move = servo_moves.Servo_moves(step_pin=step_pin, direction_pin=direction_pin, enable_pin=enable_pin)
        self.positions: dict = positions

    def move_to(self, step: str) -> None:
        if step in self.positions:
            target_pos = self.positions[step]
            current_pos = self.servo_move.get_current_pos()

            if target_pos < current_pos:
                steps = current_pos - target_pos
                self.servo_move.goLeft(steps)
            elif target_pos > current_pos:
                steps = target_pos - current_pos
                self.servo_move.goRight(steps)
            self.servo_move.set_current_pos(target_pos)
        else:
            print(f"Step {step} not found")

    def set_step_length(self, steps: int) -> None:
        self.servo_move.set_step_length(steps)

'''
if __name__ == "__main__":
    positions = {"pos1": 1, "pos2": 2}
    servo = Servo(positions=positions)
    servo.set_step_length(200)  # Set a new step length
    servo.move_to("pos1")  # Move to position VODKA
    print(servo.servo_moves.get_current_pos())  # Output: 450

    servo.move_to("pos2")  # Move to position COCA_COLA
    print(servo.servo_moves.get_current_pos())  # Output: 1350
'''