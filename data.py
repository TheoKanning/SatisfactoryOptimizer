import json

from recipe import Recipe

def load_recipes():
    with open("data.json") as f:
        data = json.load(f)

    items = data['items']
    buildings = data['buildings']
    recipes = []

    for recipe in data['recipes'].values():
        if recipe['forBuilding'] or not recipe['inMachine']:
            continue

        r = Recipe(recipe['name'], buildings[recipe['producedIn'][0]]['name'])

        multiplier = 60/recipe['time'] # convert all values to x/minute

        for item in recipe['ingredients']:
            name = items[item['item']]['name']
            r.add_input(name, item['amount']*multiplier)

        for item in recipe['products']:
            name = items[item['item']]['name']
            r.add_output(name, item['amount']*multiplier)

        recipes.append(r)

    return recipes

