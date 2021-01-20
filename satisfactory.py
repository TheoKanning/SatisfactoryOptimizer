from data import load_recipes

recipes = load_recipes()

for r in recipes:
    print(r.description())
