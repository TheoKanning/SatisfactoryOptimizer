from data import load_recipes
from recipe import optimize_recipes

recipes = load_recipes()
default_recipes = [r for r in recipes if not r.alternate]

inputs = {
    "Crude Oil": 300,
    "Water": 800,
    "Coal": 533.33,
    "Sulfur": 533.33
}
outputs = {
    "Fuel": 600,
    "Turbofuel": 2000
}

optimize_recipes(recipes, inputs, outputs)

