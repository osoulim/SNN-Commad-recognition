from code.my_neuron import MyNeuron

class Population:
    size = 0
    neurons = []

    def __init__(self, size, neuron_class=MyNeuron, layer_id=0):
        self.size = size
        for i in range(self.size):
            self.neurons.append(neuron_class(neuron_id=i, layer_id=layer_id))
    
    def __getitem__(self, key):
        return self.neurons[key]

    def reset(self):
        for neuron in self.neurons:
            neuron.reset()