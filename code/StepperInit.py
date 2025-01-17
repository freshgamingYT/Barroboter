import RPi.GPIO as GPIO
import time
import json
import os
from flask_socketio import emit

from logger import setup_logger
from fileHandler import FileHandler

class StepperInit:
    nullPos = 0
    maxPos = 0
    aktuellePos = 0

    # Pin configuration
    STEP = 17
    DIR = 27
    EN = 23
    schalterLinksPin = 16
    schalterRechtsPin = 24

    # Timing and delay
    us_delay = 950
    uS = 0.000001  # 0.00001 normal

    def __init__(self):
        self.logger = setup_logger()
        self.logger.debug("logger initialized")
        self.GPIOConfig()
        self.positionsFileHandler = FileHandler('./json/positions.json')
        self.positions = self.positionsFileHandler.readJson()
        self.initFileHandler = FileHandler('./json/stepper_init.json')
        self.initSequence = self.initFileHandler.readJson()
        self.available_cocktails_file = "./json/available_cocktails.json" 
        self.load_available_cocktails()

    def GPIOConfig(self):
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)

        GPIO.setup(self.schalterLinksPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.schalterRechtsPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.EN, GPIO.LOW)
        
        self.logger.info("Setup GPIO")

    def initMoveMotor(self, direction, stop_condition):  # stop_condition is reference to getSchalterStatus
        """Move the motor in the specified direction until the stop condition is met."""
        self.logger.debug("In initMoveMotor")

        GPIO.output(self.DIR, direction)
        while not stop_condition():
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.uS * self.us_delay)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.uS * self.us_delay)

            if direction == GPIO.HIGH:
                self.aktuellePos += 1
            else:
                self.aktuellePos -= 1

            self.logger.info(f"new aktuellePos is {self.aktuellePos}")

    def getSchalterRechtsStatus(self) -> bool:
        """Check the status of the right limit switch."""
        self.logger.info(f"status of right button {GPIO.input(self.schalterRechtsPin)}")
        return GPIO.input(self.schalterRechtsPin) == 1

    def getSchalterLinksStatus(self) -> bool:
        """Check the status of the left limit switch."""
        self.logger.info(f"status of right button {GPIO.input(self.schalterLinksPin)}")
        return GPIO.input(self.schalterLinksPin) == 1

    def init(self):
        """Execute the initialization sequence from stepper_init.json."""
        for step in self.initSequence:
            if step == "left":
                self.logger.info("Step 1: Moving left...")
                self.initMoveMotor(GPIO.LOW, self.getSchalterLinksStatus)  # Move left until left button is pressed
                self.nullPos = 0
                self.aktuellePos = 0
                self.logger.info(f"Left limit switch reached!, nullPos: {self.nullPos} ")
                time.sleep(1)
            elif step == "right":
                self.logger.info("Step 2: Moving right...")
                self.initMoveMotor(GPIO.HIGH, self.getSchalterRechtsStatus)  # Move right until right button is pressed
                self.maxPos = self.aktuellePos 
                self.logger.info(f"Right limit switch reached!, maxPos: {self.maxPos}, aktuellePos: {self.aktuellePos}")
                time.sleep(1)
            elif step == "left_again":
                self.logger.info("Step 3: Moving left again...")
                self.initMoveMotor(GPIO.LOW, self.getSchalterLinksStatus)  # Move left until left button is pressed
                self.aktuellePos = 0
                self.logger.info(f"Left limit switch reached again!, aktuellePos: {self.aktuellePos}")
                time.sleep(1)

        # Calculate maxPos as the sum of absolute values of nullPos and maxPos
        self.maxPos = abs(self.nullPos) + abs(self.maxPos) 

        # Print available positions
        print("Available Cocktails:")
        for cocktail in self.available_cocktails:
            print(f"- {cocktail}") 

        while 1:
            try:
                user_input = input("Enter cocktail name or 'q' to quit: ")
                if user_input.lower() == 'q':
                    break

                if user_input in self.available_cocktails: 
                    sequence_file = f"./json/sequences/{user_input}_sequence.json"  # Corrected file path
                    if os.path.exists(sequence_file):
                        sequence_file_handler = FileHandler(sequence_file)
                        sequence = sequence_file_handler.readJson()
                        self.execute_sequence(sequence)
                    else:
                        print(f"Error: {user_input}_sequence.json file not found.")
                else:
                    print(f"Invalid cocktail name: {user_input}")

            except KeyboardInterrupt:
                print("Exiting program...")
                break

            if (self.aktuellePos < 0) or (self.aktuellePos > self.maxPos):
                print("Limit switch triggered! Stopping motor.")
                break 

    def execute_sequence(self, sequence):
        total_steps = len(sequence)
        current_step = 0

        for position_name, wait_time in sequence.items():
            if position_name in self.positions:
                target_steps = self.positions[position_name]  # Lookup the position in positions.json
                self.move_to_position(target_steps)
                time.sleep(wait_time)  # Wait for the specified time

                # Send progress update to the client
                current_step += 1
                progress = (current_step / total_steps) * 100
                self.send_progress_update(progress)
            else:
                print(f"Invalid position in sequence: {position_name}")

            if position_name == "finished":
                print("Sequence completed. Waiting for 10 seconds...")
                time.sleep(10) 
                self.move_to_position(self.nullPos) 
                print("Returned to Null position.")
                self.send_progress_update(100)  # Ensure progress is 100% at the end
                self.send_redirect_to_index()  # Redirect to index page
                break

    def move_to_position(self, target_steps, speed='mid'):
        """Moves the motor to the specified position."""
        relative_steps = target_steps - self.aktuellePos
        self.moveRelPos(relative_steps, self.aktuellePos, speed)  # Pass aktuellePos and speed to moveRelPos
        self.aktuellePos = target_steps

    def moveRelPos(self, relative_steps, aktuellePos, speed):
        """Moves the motor by the specified relative number of steps."""
        direction = GPIO.HIGH if relative_steps > 0 else GPIO.LOW
        absolute_steps = abs(relative_steps)

        # Set speed based on the provided speed parameter
        if speed == 'fast':
            delay = self.uS * 500
        elif speed == 'slow':
            delay = self.uS * 1500
        else:
            delay = self.uS * self.us_delay

        GPIO.output(self.DIR, direction)
        for _ in range(absolute_steps):
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(delay)

            if direction == GPIO.HIGH:
                aktuellePos += 1
            else:
                aktuellePos -= 1

            if (aktuellePos < 0) or (aktuellePos > self.maxPos):
                print("Limit switch triggered! Stopping motor.")
                break

        self.aktuellePos = aktuellePos 

    def load_available_cocktails(self):
        try:
            with open(self.available_cocktails_file, 'r') as f:
                self.available_cocktails = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {self.available_cocktails_file} not found. Creating default file.")
            self.available_cocktails = []
            self.save_available_cocktails()

    def save_available_cocktails(self):
        with open(self.available_cocktails_file, 'w') as f:
            json.dump(self.available_cocktails, f, indent=4)

    def send_progress_update(self, progress):
        emit('progress_update', {'progress': progress}, broadcast=True, namespace='/')

    def send_redirect_to_index(self):
        emit('redirect_to_index', {}, broadcast=True, namespace='/')

if __name__ == "__main__":
    try:
        stepper = StepperInit()
        stepper.init()
    except Exception as e:
        print(e)
