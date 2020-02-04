import numpy as np
import math
from Synapse import Synapse
import parameters

class MySynapses(Synapse):

	def __init__(self, pre_neurons = list(), post_neurons = list()):
		super().__init__(pre_neurons, post_neurons)
		homeostasis_scale = 4/parameters.nDots
		learning_scale = 2/parameters.nDots

		self.weight = np.random.normal(0.95, 0.05)
		self.delay = np.random.normal(50, 0.02)
		self.number_of_spikes = 0
		self.last_update_time = -1
		self.cnt = 0 
		self.is_freezed = False
		# self.feature = feature


		#STDP parameters
		self.tau_pre = 5.0 
		self.tau_post = 5.0 
		self.cApre = 4e-4 * learning_scale 
		self.cApost = 5e-4 * learning_scale
		self.wmax = 1
		self.wmin = 0
		self.eps_weight_decay = 1e-4 * learning_scale
	
		#delay_parameters
		self.A_pre = (2*0.05-1e-4) * learning_scale *4
		self.A_post = 2*0.05 * learning_scale *4
		self.B = 5.0 #
		self.dmax = 100
		self.dmin = 0
		self.eps_delay_decay = 1e-4 * learning_scale *4
		self.ddelay = 0

		#homeostasis_parameters
		self.Hd = 0.05 * homeostasis_scale * parameters.nPatterns*parameters.coherence /2
		self.Hw = 5e-4 * homeostasis_scale * parameters.nPatterns*parameters.coherence /2
		self.Hwindow = parameters.size_of_data
		self.target = parameters.nDots * parameters.coherence * self.Hwindow /parameters.nPatterns
		self.nspike_list = [self.target/self.Hwindow for i in range(self.Hwindow)]
		self.observe = self.target


	def disable_learing(self):
		self.is_freezed = True

	def add_connection(self, pre_neuron, post_neuron):
		self.pre_neurons.append(pre_neuron)
		self.post_neurons.append(post_neuron)
		pre_neuron.forward_neurons.append(post_neuron)
		post_neuron.back_neurons.append(pre_neuron)
		pre_neuron.forward_synapses.append(self)
		post_neuron.back_synapses.append(self)

	def STDP(self, pre_neuron, post_neuron ):
		if self.is_freezed:
			return 0

		if pre_neuron.spike_time == -1:
			self.weight = max(self.wmin, self.weight-self.eps_weight_decay)
			return 0
		delta_time = post_neuron.get_spike_time() - pre_neuron.get_spike_time() - self.delay +1e-9
		if(delta_time >= 0):
			self.weight = np.clip(self.weight + (self.cApost*math.exp( -(delta_time)/self.tau_post)) , self.wmin , self.wmax)	
		else:
			self.weight = np.clip(self.weight - (self.cApre*math.exp( (delta_time) /self.tau_pre )) , self.wmin , self.wmax)
	
	def delay_plasticity(self, pre_neuron, post_neuron):

		self.number_of_spikes += 1
		if pre_neuron.spike_time == -1:
			self.ddelay += self.eps_delay_decay
			return 0
		delta_time = post_neuron.get_spike_time() - pre_neuron.get_spike_time() - self.delay + 1e-9
		if(delta_time >= 0):
			self.ddelay += -self.A_post*math.exp( -(delta_time)/self.B)
		else:
			self.ddelay += self.A_pre*math.exp( (delta_time)/self.B)

		return 0
	
	def homeostasis(self):
		target = parameters.nDots * parameters.coherence * self.Hwindow /parameters.nPatterns
		observe = self.observe

		# if(self.cnt % 50 == 0):
		# 	print(self.feature, target, observe, self.cnt)
		# 	print(self.weight, self.delay)
		# 	print("**************")

		#homeostasis on delay
		normal_delay_inc = (self.delay-self.dmin)/(self.dmax-self.dmin)
		normal_delay_dec = (self.delay-self.dmin)/(self.dmax-self.dmin)
		if(target > observe):
			self.delay = np.clip(self.delay - normal_delay_dec*self.Hd*(target-observe)/target, self.dmin, self.dmax)
		else:
			self.delay = np.clip(self.delay - normal_delay_dec*self.Hd*(target-observe)/target, self.dmin, self.dmax)

		#homeostasis on weight
		self.weight = np.clip(self.weight + self.Hw*(target-observe)/target, self.wmin, self.wmax)

		return 0
	
	def reset(self):
		self.cnt+=1
		self.nspike_list.append(self.number_of_spikes)
		self.observe+=self.number_of_spikes
		learning_rate = 1/math.pow(self.cnt, 0.46)
		if not self.is_freezed:
			self.delay = np.clip(self.delay+learning_rate*self.ddelay, self.dmin, self.dmax)
		
		self.observe-=self.nspike_list[0]
		self.nspike_list = self.nspike_list[1:]
		if not self.is_freezed:
			self.homeostasis()
		
		self.number_of_spikes = 0
		self.ddelay = 0
