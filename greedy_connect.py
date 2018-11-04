import numpy as np

def greedy_solution_sens(data):
	""" this funcion is used to create a solution for the detection constraint (but not the communication)
	it's greedy because we try to add the target with the bigger number of undetected neighbours. """ 
	n = data.get_size()
	nb_neighbours = np.zeros(n)
	sensors = set()
	neighbours = {}
	already_visited = set()
	for i in range(n):
		neighbours[i] = set(data.get_neighbours_sens(i))
		neighbours[i].remove(i)
		nb_neighbours[i] = len(neighbours[i])

	while len(already_visited) < n:
		new_sensor = np.argmax(nb_neighbours)
		sensors.add(new_sensor)
		already_visited.add(new_sensor)
		for i in neighbours[new_sensor]:
			already_visited.add(i)
			if new_sensor in neighbours[i]:
				neighbours[i].remove(new_sensor)
			for j in neighbours[i]:
				if i in neighbours[j]:
					neighbours[j].remove(i) 
		neighbours[new_sensor] = set()
		nb_neighbours = [len(neighbours[i]) for i in range(n)]
	return sensors


	