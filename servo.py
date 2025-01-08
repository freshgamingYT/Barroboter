from movement import Movement

class Servo:
    def __init__(self, positions: dict, step_pin: int, direction_pin: int, enable_pin: int, socketio, velocity_settings: dict, distance_thresholds: dict):
        self.movement = Movement(step_pin=step_pin, direction_pin=direction_pin, enable_pin=enable_pin, socketio=socketio, velocity_settings=velocity_settings)
        self.positions = positions
        self.velocity_settings = velocity_settings
        self.distance_thresholds = distance_thresholds

    def move_to(self, step: str) -> None:
        if step in self.positions:
            target_pos = self.positions[step]
            current_pos = self.movement.get_current_pos()

            distance = abs(target_pos - current_pos)
            if distance == 0:
                velocity = 0
            elif distance <= self.distance_thresholds['threshold_1']:
                velocity = 1
            elif distance <= self.distance_thresholds['threshold_2']:
                velocity = 2
            else:
                velocity = 3

            self.movement.set_velocity(velocity)
            self.movement.move_to_position(target_pos)
        else:
            print(f"Step {step} not found")

    def cleanup(self):
        self.movement.cleanup()
