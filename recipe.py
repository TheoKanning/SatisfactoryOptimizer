
class Recipe:
    """ Represents the inputs, outputs, etc for a single recipe """

    def __init__(self, name: str, building: str, alternate=False):
        self.name = name
        self.building = building
        self.inputs = {}
        self.outputs = {}
        self.alternate = alternate

    def add_input(self, name: str, quantity: float):
        self.inputs[name] = quantity

    def add_output(self, name: str, quantity: float):
        self.outputs[name] = quantity

    def products_used(self):
        return set(self.inputs.keys()).union(set(self.outputs.keys()))

    def product_net_quantity(self, product: str):
        net = 0

        if product in self.inputs:
            net -= self.inputs[product]
        if product in self.outputs:
            net += self.outputs[product]

        return net

    def description(self):
        input_str = '\n\t'.join([f"{q} {i}" for i, q, in self.inputs.items()])
        output_str = '\n\t'.join([f"{q} {i}" for i, q, in self.outputs.items()])
        return f"{self.name}\nProduced in: {self.building}\nInputs:\n\t{input_str}\nOutputs:\n\t{output_str}"

    def __str__(self):
        return self.name
