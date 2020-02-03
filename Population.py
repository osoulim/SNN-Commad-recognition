from code.my_neuron import MyNeuron

class Population:
    size = 0
    neurons = []

    def __init__(self, size, neuron_class=MyNeuron):
        self.size = size
        for i in range(self.size):
            self.neurons.append(neuron_class())
    
    def __getitem__(self, key):
        return self.neurons[key]