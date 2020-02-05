class Population:

    def __init__(self, size, layer_id, neuron_class):
        self.neurons = list()
        for i in range(size):
            self.neurons.append(neuron_class(neuron_id=i, layer_id=layer_id))

    def __getitem__(self, key):
        return self.neurons[key]

    def reset(self):
        for neuron in self.neurons:
            neuron.reset()