import json
from logger import setup_logger

class FileHandler:
    def __init__(self, filePath):
        self.logger = setup_logger()
        self.filePath = filePath
        self.data = self.readJson()
        
    def readJson(self):
        with open(self.filePath, 'r') as file:
            data = json.load(file)
            self.logger.debug("successfully loaded JsonFile for Positions")
        return data
    
    def updateJson(self, newValue):
        self.data["Endpoint"] = newValue
        with open(self.filePath, 'w') as file:
            json.dump(self.data, file, indent=4)
            self.logger.debug("Successfully updated Endpoint with new Endpoint")
