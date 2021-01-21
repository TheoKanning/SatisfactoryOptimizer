from ortools.linear_solver import pywraplp

"""
Class that finds a product setup to maximize desired output components given input constraints
"""


class Optimizer:
    def __init__(self, recipes, inputs, outputs):
        """
        :param recipes: List of available recipes
        :param inputs: dict of available input components and rates in x/min, {"Iron Ore": 30}
        :param outputs: dict of desired outputs and scores {"Fuel": 600, "Turbofuel": 2000}
                        all other products will have a score of 0
        """
        self.recipes = recipes
        self.inputs = inputs
        self.outputs = outputs
        self.recipe_max = 100
        self.component_max = 10000
        self.recipe_cost = 0.01  # small cost to encourage fewer recipes overall

    def optimize(self):
        components = list(set([c for recipe in self.recipes for c in recipe.components_used()]))
        components.sort()

        solver = pywraplp.Solver.CreateSolver('GLOP')
        recipe_vars = dict([(r.name, solver.NumVar(0, self.recipe_max, r.name)) for r in self.recipes])

        # for each component, add a constraint that the total amount is at least zero
        for component in components:
            min_value = -self.inputs[component] if component in self.inputs else 0
            ct = solver.Constraint(min_value, self.component_max, component)

            # add the contribution of each recipe
            for i, recipe in enumerate(self.recipes):
                ct.SetCoefficient(recipe_vars[recipe.name], recipe.component_net_quantity(component))

        # the objective function is the total score of all outputs created by each recipe
        objective = solver.Objective()
        for i, recipe in enumerate(self.recipes):
            recipe_contribution = sum([recipe.component_net_quantity(c) * s for c, s in self.outputs.items()])
            recipe_contribution -= self.recipe_cost
            objective.SetCoefficient(recipe_vars[recipe.name], recipe_contribution)

        objective.SetMaximization()

        solver.Solve()

        print('Solution:')
        print(f"Objective value: {objective.Value():.2f}")

        print("\nRecipes Used:")
        for recipe in self.recipes:
            var = recipe_vars[recipe.name]
            if var.solution_value():
                print(f"{recipe.name}: {var.solution_value():.2f}")

        print("\nInputs Remaining:")
        for c, q in self.inputs.items():
            for recipe in self.recipes:
                q += recipe.component_net_quantity(c) * recipe_vars[recipe.name].solution_value()

            print(f"{c}: {q:.2f}")

        # outputs created
        print("\nProduced Components:")
        for c in components:
            q = 0
            for recipe in self.recipes:
                q += recipe.component_net_quantity(c) * recipe_vars[recipe.name].solution_value()

            if q > 0.01:
                print(f"{c}: {q:.2f}")
