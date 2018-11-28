from peewee import IntegerField, Model, PrimaryKeyField, CharField, SqliteDatabase, ForeignKeyField
from playhouse.shortcuts import model_to_dict
from lib.config import db

class PitenderModel(Model):
    id = PrimaryKeyField(null=False)

    class Meta:
        database = db

class Ingredient(PitenderModel):
    name = CharField(null=False)
    shortname = CharField(null=False)

class PumpConfig(PitenderModel):
    pin = IntegerField(null=False)
    ingredient = ForeignKeyField(Ingredient, backref='pump_configs')
    flow_rate = IntegerField(null=False)

class Drink(PitenderModel):
    name = CharField(null=False)

class RecipeStep(PitenderModel):
    order = IntegerField(null=False)
    drink = ForeignKeyField(Drink, backref='recipe_steps')
    delay_after = IntegerField(null=True)

class RecipeIngredientInstruction(PitenderModel):
    volume = IntegerField(null=False)
    delay = IntegerField(null=True)
    ingredient = ForeignKeyField(Ingredient)
    recipe_step = ForeignKeyField(RecipeStep, backref='recipe_ingredient_instructions')

