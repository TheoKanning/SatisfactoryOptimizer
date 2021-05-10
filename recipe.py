from ortools.linear_solver import pywraplp
from typing import List, Dict

from common import Recipe


def optimize_recipes(recipes: List[Recipe], inputs: Dict[str, int], outputs: Dict[str, float]):
    """
    Finds recipe ratios to maximize desired output products given input resource constraints
    :param recipes: List of available recipes
    :param inputs: dict of available input products and rates in x/min, {"Iron Ore": 30}
    :param outputs: dict of desired outputs and scores {"Fuel": 600, "Turbofuel": 2000}
                    all other products will have a score of 0
    """
    validate_products(list(inputs.keys()), recipes)
    validate_products(list(outputs.keys()), recipes)
    recipe_max = 100
    product_max = 10000
    recipe_cost = 0.01  # small cost to encourage fewer recipes overall

    products = list(set([c for recipe in recipes for c in recipe.products_used()]))
    products.sort()

    solver = pywraplp.Solver.CreateSolver('GLOP')
    recipe_vars = dict([(r.name, solver.NumVar(0, recipe_max, r.name)) for r in recipes])

    # for each product, add a constraint that the total amount is at least zero
    for product in products:
        min_value = -inputs[product] if product in inputs else 0
        ct = solver.Constraint(min_value, product_max, product)

        # add the contribution of each recipe
        for recipe in recipes:
            ct.SetCoefficient(recipe_vars[recipe.name], recipe.product_net_quantity(product))

    # the objective function is the total score of all outputs created by each recipe
    objective = solver.Objective()
    for recipe in recipes:
        recipe_contribution = sum([recipe.product_net_quantity(c) * s for c, s in outputs.items()])
        recipe_contribution -= recipe_cost
        objective.SetCoefficient(recipe_vars[recipe.name], recipe_contribution)

    objective.SetMaximization()

    solver.Solve()

    print('Solution:')
    print(f"Objective value: {objective.Value():.2f}")

    print("\nRecipes Used:")
    for recipe in recipes:
        var = recipe_vars[recipe.name]
        if var.solution_value():
            print(f"{recipe.name}: {var.solution_value():.2f}")

    print("\nInputs Remaining:")
    for p, q in inputs.items():
        for recipe in recipes:
            q += recipe.product_net_quantity(p) * recipe_vars[recipe.name].solution_value()

        print(f"{p}: {q:.2f}")

    print("\nProduced:")
    for p in products:
        q = 0
        for recipe in recipes:
            q += recipe.product_net_quantity(p) * recipe_vars[recipe.name].solution_value()

        if q > 0.01:
            print(f"{p}: {q:.2f}")


def validate_products(products: List[str], recipes: List[Recipe]):
    unknown_products = []
    all_products = list(set([c for recipe in recipes for c in recipe.products_used()]))

    for product in products:
        if product not in all_products:
            unknown_products.append(product)

    for product in unknown_products:
        print(f"Could not find product \"{product}\"")
