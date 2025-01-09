from flask import Flask, render_template, request
import RPi.GPIO as GPIO
from config import Config
from barroboter import Barroboter
import signal_helper  # Import the signal helper to set up the signal handler

app = Flask(__name__)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Load configuration
config = Config('json/config.js')
barroboter = Barroboter(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    barroboter.load_positions('json/Cocktails/positions.js')
    barroboter.load_ingredients('json/Cocktails/ingredients/cocktail1_ingredients.js')
    barroboter.start()
    return 'Process completed'

if __name__ == '__main__':
    app.run(debug=True)
