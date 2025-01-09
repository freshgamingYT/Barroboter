from flask import Flask, render_template, request
import RPi.GPIO as GPIO
from config import Config
from barroboter import Barroboter
import signal_helper  # Import the signal helper to set up the signal handler

app = Flask(__name__)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Load configuration
config = Config('json/config.json')
barroboter = Barroboter(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    drink_name = request.form['drink_name']
    print(f"Selected drink: {drink_name}")
    barroboter.load_positions('json/Cocktails/positions.json')
    barroboter.load_ingredients(f'json/Cocktails/ingredients/{drink_name}_ingredients.json')
    barroboter.start()
    return 'Process completed'

if __name__ == '__main__':
    app.run(debug=True)
