
class Neuron:

	def __init__(self):
		self.threshold = 25
		self.tm = 2500
		self.current_v = 0
		self.last_update_time = 0
		self.spike_time = -1

	def spike(self):
		self.current_v = 0
		
	def check_spike(self):
		return self.current_v > self.threshold

	def excite(self, v):
		self.current_v+=v

	def update(self, t):
		self.last_update_time = t
