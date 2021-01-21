# Satisfactory Optimization
This project uses Google's [OR-Tools](https://developers.google.com/optimization) to find optimal production ratios 
in [Satisfactory](http://www.satisfactorygame.com).

Data taken from https://raw.githubusercontent.com/greeny/SatisfactoryTools/dev/data/data.json

## Recipes
Satisfactory is a game of building advanced components from simple building blocks.
For example, Iron Ore becomes Iron Ingots, and Iron Ingots become Iron Plates. 

## Usage
Load recipes from the data file. For simplicity this example only uses default recipes. 
```
recipes = load_recipes()
default_recipes = [r for r in recipes if not r.alternate]
```

Specify the available resources in units/minute.  
```
inputs = {
    "Iron Ore": 60
}
```

Give a positive score to components you want to create.
```
outputs = {
    "Reinforced Iron Plate": 1
}
```

Run the optimizer
```
optimizer = Optimizer(default_recipes, inputs, outputs)
optimizer.optimize()
```

Output:
```
Solution:
Objective value: 4.93

Recipes Used:
Iron Ingot: 2.00
Reinforced Iron Plate: 1.00
Iron Plate: 1.50
Iron Rod: 1.00
Screw: 1.50

Inputs Remaining:
Iron Ore: 0.00

Produced Components:
Reinforced Iron Plate: 5.00
```
`Recipes Used` shows how many machines need to run each recipe.  
`Inputs Remaining` shows which resources run out first and limit production.  
`Produced Components` shows all the produced components, not just those with a score.

## Linear Optimization
I modelled the recipe production ratios as a [linear programming](https://www.analyticsvidhya.com/blog/2017/02/lintroductory-guide-on-linear-programming-explained-in-simple-english/) problem.  
Linear programming allows us to optimize a linear objective function within a set of constraints.  
The objective function and constraints must be expressed as a set of equations using decision variables.  
The linear programming problem can return decimal values, which works fine for Satisfactory and takes much less time to solve.

### Objective Function
An _objective function_ is a linear equation that the minimizer attempts to maximize (or minimize).  
The optimizer takes a score for every desired product and attempts to maximize its score.

### Decision Variables
The optimizer modifies _decision variables_ in order to maximize its objective function.  
In this case, the decision variables are the number of machines producing each recipe.

x<sub>r</sub> = # of instances of recipe _r_
### Constraints
_Constraints_ are conditions that restrict the final output.
For this problem, the only constraint is that each component has a non-negative quantity, otherwise the optimizer could use recipes without having prerequisite materials. 

n<sub>cr</sub> = number of component _c_ produced by recipe _r_, will be negative if _c_ is an input to _r_

For each _c_,  
n<sub>c1</sub>x<sub>1</sub> + n<sub>c2</sub>x<sub>2</sub> + ... + n<sub>cr</sub>x<sub>r</sub> >= 0