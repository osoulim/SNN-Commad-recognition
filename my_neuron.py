import numpy as np
import math
from Neuron import Neuron
import parameters

class MyNeuron(Neuron):

	def __init__(self, neuron_id, layer_id):
		self.threshold = 4.16
		self.tm = 24
		self.current_v = 0
		self.last_update_time = 0
		self.spike_time = -1
		self.forward_neurons = list()
		self.forward_synapses= list()
		self.back_neurons = list()
		self.back_synapses= list()
		self.cnt = 0
		self.r_min = -0.10
		self.r_max = 0.10
		self.r_d = 0.00025
		self.r_current = 0
		self._id = neuron_id
		self.layer_id = layer_id
	
	def spike(self):
		self.current_v = 0
		self.spike_time = self.last_update_time
		app = list()
		for i in range(len(self.back_neurons)):
			neuron = self.back_neurons[i]
			synapse = self.back_synapses[i]
			synapse.STDP(neuron, self)
			synapse.delay_plasticity(neuron, self)
			
		for i in range(len(self.forward_neurons)):
			neuron = self.forward_neurons[i]
			synapse = self.forward_synapses[i]
			if(neuron.spike_time != -1):
				synapse.number_of_spikes-=1
				synapse.STDP(self, neuron)
				synapse.delay_plasticity(self, neuron)
			app.append((self.spike_time+synapse.delay, synapse.weight,
					 neuron.layer_id, neuron._id))

		return app

	def get_spike_time(self):
		return self.spike_time

	def check_spike(self):
		return (self.current_v  > self.threshold+ self.r_current+ (np.random.random()*0.1 - 0.05)) and (self.spike_time==-1)
		return (self.current_v  > self.threshold+ self.r_current) and (self.spike_time==-1)

	def excite(self, v):
		self.current_v+=v
		if self.check_spike():
			return self.spike()
		return list()
	
	def update(self, time):
		if(self.last_update_time >= time):
			return 
		self.current_v 	= self.current_v*math.exp(-(time-self.last_update_time)/self.tm)
		self.last_update_time = time

	def reset(self):
		if(self.cnt > parameters.size_of_data):
			if(self.spike_time == -1):
				if(self.r_current-self.r_d >= self.r_min):
					self.r_current = self.r_current-self.r_d
			else:
				if(self.r_current+self.r_d <= self.r_max):
					self.r_current = self.r_current+self.r_d

		self.cnt+=1
		self.current_v = 0
		self.last_update_time = 0
		self.spike_time = -1
		