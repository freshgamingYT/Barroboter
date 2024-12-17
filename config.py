
import json

class ConfigManager:
    def __init__(self, step_pin: int, direction_pin: int, enable_pin: int, pos=0, steps=200, us_delay=950, uS=0.000001, moving=False, max_steps=4050):
        self.step_pin: int = step_pin
        self.direction_pin: int = direction_pin
        self.enable_pin: int = enable_pin
        self.pos: int = pos
        self.steps: int = steps
        self.us_delay: int = us_delay
        self.uS: float = uS
        self.moving: bool = moving
        self.max_steps: int = max_steps

    def save_to_json(self, filename):
        data = {
            "step_pin": self.step_pin,
            "direction_pin": self.direction_pin,
            "enable_pin": self.enable_pin,
            "pos": self.pos,
            "steps": self.steps,
            "us_delay": self.us_delay,
            "uS": self.uS,
            "moving": self.moving,
            "max_steps": self.max_steps
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.step_pin = data["step_pin"]
            self.direction_pin = data["direction_pin"]
            self.enable_pin = data["enable_pin"]
            self.pos = data["pos"]
            self.steps = data["steps"]
            self.us_delay = data["us_delay"]
            self.uS = data["uS"]
            self.moving = data["moving"]
            self.max_steps = data["max_steps"]
