import json

class Config:
    def __init__(self, config_path):
        with open(config_path) as config_file:
            self.data = json.load(config_file)
