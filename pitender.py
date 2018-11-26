from flask import Flask, jsonify, abort
from lib.config import db
from lib.ingredient import ingredients
from lib.routes.drinks import drink_routes
from lib.models import Drink, RecipeIngredientInstruction, RecipeStep, Ingredient, PumpConfig
from threading import Thread, Lock
from playhouse.shortcuts import model_to_dict
import json
import time
import signal
import sys
import RPi.GPIO as GPIO

busy_lock = Lock()

app = Flask(__name__)
app.register_blueprint(ingredients)
app.register_blueprint(drink_routes)

# SETUP pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for c in PumpConfig.select():
    GPIO.setup(c.pin, GPIO.OUT)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

busy = False

@app.route("/make_drink/<id>")
def make(id):
    global busy
    with busy_lock:
        if busy is True:
            return "busy"
    
    drink = Drink.get_or_none(id=id)

    if drink is None:
        abort(404)

    with busy_lock:
        busy = True
    drink_thread = Thread(target=make_drink, args=[drink])
    drink_thread.start()

    return "Start making drink {}".format(drink.name)

def make_drink(drink: Drink):
    global busy
    
    print("START: Drink {}".format(drink.name))

    for step in drink.recipe_steps.order_by(RecipeStep.order.asc()):
        step_threads = []
        print("START: STEP #{}".format(step.order))
        for instruction in step.recipe_ingredient_instructions:
            t = Thread(target=handle_instruction,args=[instruction])
            t.start()
            step_threads.append(t)
        for thread in step_threads:
            thread.join()
        if step.delay_after is not None:
            print("Pausing for {}s after Step #{}".format(step.delay_after/1000, step.order))
            time.sleep(step.delay_after/1000)
        print("DONE: STEP #{}".format(step.order))
    with busy_lock:
        busy = False
    print("DONE: Drink {}".format(drink.name))


def handle_instruction(instruction: RecipeIngredientInstruction):
    pump_configs = instruction.ingredient.pump_configs
    num_pumps = pump_configs.count()
    # 100ml pro min in sec
    time_needed = instruction.volume/100*60/num_pumps

    print("START: Pouring {}ml of {} over a period of {}s from {} pump(s)".format(instruction.volume, instruction.ingredient.name, time_needed, num_pumps))

    for pump in pump_configs:
        # GPIO(pin) => HIGH
        GPIO.output(pump.pin, GPIO.HIGH)
        print("PUMP PIN #{} ({}): ACTIVATE".format(pump.pin, instruction.ingredient.name))
    
    time.sleep(time_needed)

    for pump in pump_configs:
        # GPIO(pin) => LOW
        GPIO.output(pump.pin, GPIO.LOW)
        print("PUMP PIN #{} ({}): DEACTIVATE".format(pump.pin, instruction.ingredient.name))

    print("DONE: {}ml of {}".format(instruction.volume, instruction.ingredient.name))
