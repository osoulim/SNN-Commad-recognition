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
        for _id, x in enumerate(self.layers_sizes):
            self.layers.append(Population(x, layer_id=_id))
        for i in range(layers_num - 1):
            for x in range(self.layers_sizes[i]):
                for y in range(self.layers_sizes[i + 1]):
                    synapses[(x, y)] = MySynapses([self.layers[i][x]], [self.layers[i+1][y]])
    
    def add_spike_to_input(self, neuron_id, time):
        self.spikes.put((time, 100, 0, neuron_id))
    
    def next_step(self):
        self.time += 1
        while len(self.spikes) > 0 and self.spikes[0][0] <= self.time:
            spike_time, exc, layer_id, neuron_id = self.spikes.get()
            if spike_time < self.time:
                continue
            next_spikes = self.layers[layer_id][neuron_id].excite(exc)
            for spike in next_spikes:
                self.spikes.put(spike)
    
    def reset(self):
        for layer in self.layers:
            layer.reset()
        for synapse in self.synapses.values():
            synapse.reset()

