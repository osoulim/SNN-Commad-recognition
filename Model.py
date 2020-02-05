from heapq import heappush, heappop
from Population import Population
from my_synapse import MySynapse
from my_neuron import MyNeuron


class Model:

    def __init__(self):
        pass

    def __init__(self, layers_sizes, neuron_class=MyNeuron, synapse_class=MySynapse):
        self.is_testing = False
        self.layers = list()
        self.synapses = {}
        self.spikes = []
        self.layers_sizes = layers_sizes
        self.layers_num = len(layers_sizes)
        for _id, x in enumerate(self.layers_sizes):
            tmp = Population(x, _id, neuron_class)
            self.layers.append(tmp)
        for i in range(self.layers_num - 1):
            for x in range(self.layers_sizes[i]):
                for y in range(self.layers_sizes[i + 1]):
                    self.synapses[(x, y)] = synapse_class()
                    self.synapses[(x, y)].add_connection(self.layers[i][x], self.layers[i+1][y])
        
    def add_spike_to_input(self, neuron_id, time):
        heappush(self.spikes, (time, 100, 0, neuron_id))
    
    def next_step(self):
        # print("Sag:", self.time, self.layers[0][0].current_v, self.synapses[(0, 0)].weight, self.synapses[(0, 0)].delay, self.layers[1][0].current_v)
        spike_time, exc, layer_id, neuron_id = heappop(self.spikes)
        # if self.is_testing:
        #     print(spike_time, exc, layer_id, neuron_id)
        spiked_neuron = self.layers[layer_id][neuron_id]
        spiked_neuron.update(spike_time)
        next_spikes = spiked_neuron.excite(exc)
        for spike in next_spikes:
            heappush(self.spikes, spike)
        
        if layer_id == self.layers_num - 1 and self.is_testing:
            print("Neuron %d spiked at %f time." % (neuron_id, spike_time))
    
    def reset(self):
        for layer in self.layers:
            layer.reset()
        for synapse in self.synapses.values():
            synapse.reset()

    def disable_learning(self):
        self.is_testing = True
        for synapse in self.synapses.values():
            synapse.disable_learing()

    def is_queue_empty(self):
        return len(self.spikes) == 0

