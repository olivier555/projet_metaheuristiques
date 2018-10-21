"""
This class describes a solution (wihtout considering the data)
"""

import numpy as np

class Solution():
	def __init__(self, n, sensors = None):
		if sensors is None:
			sensors = np.zeros(n,dtype = 'bool')
		else:
			sensors = np.array(sensors,'bool')
			assert sensors.size == n, "size of sensors must be equal to n %s"%n
		self.sensors = sensors
		self.value = self.compute_value()

	def compute_value(self):
		return sum(self.sensors == 1)

	def detected(self, data):
		M = data.get_matrix_sens()
		return (np.matmul(M, self.sensors)[1:] >= 1).all()
		# we want all the targets to be detected except the hole


	def related(self, data):
		reached = {0}
		next_vertex = set(data.neighbours(0))
		index_sensors = np.where(sensors)
		while len(next_vertex) > 0 and len(reached) < self.value:
			v = set([])
			for i in next_vertex :
				new = intersection(set(data.neighbours_sens(i)),index_sensors)
				new = new - reached
				reached = union(reached,new)
				v = v.union(new)
			next_vertex = v
		return len(reached) == self.value + (1 - self.sensors[0])
		# we want to reach all the sensors from the hole, but we don't want
		# to count the hole twice if it's a sensor


	def eligible(self, data):
		return self.detected(data) and self.related(data)

	def add_sensor(self,i):
		if not self.sensors[i]:
			self.sensors[i] = True
			self.value += 1

	def remove_sensor(self,i):
		if self.sensors[i]:
			self.sensors[i] = False
			self.value -= 1

	def is_sensor(self,i):
		return self.sensors[i]

	def get_index_sensors(self):
		return list(np.where(self.sensors)[0])


if __name__ == '__main__':
	s = Solution(5,[True, True, True, True ,True])
	s = Solution(5)