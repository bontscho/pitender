from flask import Blueprint, jsonify, request
from lib.config import db
import json
from peewee import Model, PrimaryKeyField, CharField
from playhouse.shortcuts import model_to_dict

ingredients = Blueprint('ingredient', __name__)

class Ingredient(Model):
    id = PrimaryKeyField(null=False)
    name = CharField(null=False)
    shortname = CharField(null=False)

    class Meta:
        database = db

@ingredients.route('/ingredients', methods=["GET"])
def index():
    query = Ingredient.select()
    return jsonify([model_to_dict(user) for user in query])
