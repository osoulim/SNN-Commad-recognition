from queue import PriorityQueue
from code.Population import Population
from code.my_synapse import MySynapses

class Model:
    layers = []
    layers_sizes = []
    layers_num = 0
    synapses = {}
    spikes = None
    time = 0

    def __init__(self):
        pass

    def __init__(self, layers_sizes):
        self.layers_sizes = layers_sizes
        self.layers_num = len(layers_sizes)
        self.spikes = PriorityQueue(sum(self.layers_sizes) * 10)
        for x in self.layers_sizes:
            self.layers.append(Population(x))
        for i in range(layers_num - 1):
            for x in range(self.layers_sizes[i]):
                for y in range(self.layers_sizes[i + 1]):
                    synapses[(x, y)] = MySynapses([self.layers[i][x]], [self.layers[i+1][y]])
    
    def add_spike(self, layer_id, neuron_id, time):
        self.spikes.put((time, layer_id, neuron_id))
    
    def next_step():
        self.time += 1
        while self.spikes[0][0] <= self.time:
            spike_time, spike = self.spikes.get()
            if spike_time < self.time:
                continue
            # TODO: spike that :DD
