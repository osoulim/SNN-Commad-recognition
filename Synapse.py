
class Synapse:

	def __init__(self, pre_neuron, post_neuron):
		self.weight = 0
		self.delay = 0
		self.pre_neuron = pre_neuron
		self.post_neuron = post_neuron
