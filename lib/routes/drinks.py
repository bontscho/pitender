from flask import Blueprint, jsonify, request
from lib.config import db
import json
from playhouse.shortcuts import model_to_dict
from lib.models import Drink

drink_routes = Blueprint('drinks', __name__)

@drink_routes.route('/drinks', methods=["GET"])
def index():
    drinks = Drink.select()
    return jsonify([model_to_dict(drink, backrefs=True) for drink in drinks])
