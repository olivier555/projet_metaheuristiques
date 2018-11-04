import numpy as np
from solution import Solution
from data import Data
from graph import Graph
from timeit import default_timer as timer
############ the three following functions are not used anymore, because they are time consuming. #############################
# There were trying to restore the connectivity constraint.

def min_number_capt_to_add(s,data):
    """ compute the minimum targets to add between two points to make them connected targets
    """
    index_sensors = s.get_index_sensors()
    n_points = s.get_size()
    M_list = [[None for j in range(n_points)] for i in range(n_points)]
    M_numbers = [[None for j in range(n_points)] for i in range(n_points)]
    neighbours = [data.get_neighbours_com(i) for i in range(n_points)]
    
    for i in range(n_points):
        already_visited = set([i])
        for j in index_sensors:
            if M_numbers[j][i] != None:
                M_numbers[i][j] = M_numbers[j][i]
                M_list[i][j] = M_list[j][i]
                already_visited.add(j)


        if s.is_sensor(i):
            d = 0
            M_list[i][i] = []
        else : 
            d = 1
            M_list[i][i] = [i]
        M_numbers[i][i] = d
        n = set([i])
        # firts research
        already_visited = set([i])
        n = set(neighbours[i]) - set(index_sensors)
        l = set(neighbours[i]).intersection(set(index_sensors)) - already_visited
        for j in n:
            M_numbers[i][j] = 1
            M_numbers[j][i] = 1
            M_list[i][j] = [j]
            M_list[j][i] = [j]
        for j in l:
            M_numbers[i][j] = 0
            M_numbers[j][i] = 0
            M_list[i][j] = []#[j]
            M_list[j][i] = []#[j]
        already_visited = already_visited.union(l)
        already_visited = already_visited.union(n)
        #depth first research
        while len(l) > 0:
            l2 = set()
            for j in l:
                n2 = set(neighbours[j]) - set(index_sensors) - already_visited
                n = n.union(n2)
                l2 = l2.union(set(neighbours[j]).intersection(set(index_sensors)) - already_visited)                
                for k in l2:
                    M_numbers[i][k] = 0
                    M_numbers[k][i] = 0
                    M_list[i][k] = M_list[i][j] #+ [k]
                    M_list[k][i] = M_list[j][i]
                for k in n2:
                    M_numbers[i][k] = 1
                    M_numbers[k][i] = 1
                    M_list[i][k] = M_list[i][j] + [k]
                    M_list[k][i] = M_list[i][j] + [k]
            already_visited = already_visited.union(l2)
            l = l2
        already_visited = already_visited.union(n)
        while None in M_numbers[i]:
            d+=1
            n4 = set()
            for j in n:
                # descente j 
                n2 = set(neighbours[j]) - set(index_sensors) - already_visited
                l = set(neighbours[j]).intersection(set(index_sensors)) - already_visited
                for k in n2:
                    M_numbers[i][k] = d + 1
                    M_numbers[k][i] = d + 1
                    M_list[i][k] = M_list[i][j] + [k]
                    M_list[k][i] = M_list[i][j] + [k]
                for k in l:
                    M_numbers[i][k] = d
                    M_numbers[k][i] = d
                    M_list[i][k] = M_list[i][j] #+ [k]
                    M_list[k][i] = M_list[i][j]
                while len(l) > 0:
                    l2 = set()
                    for k in l:
                        n3 = set(neighbours[k]) - set(index_sensors) - already_visited
                        n2 = n2.union(n3)
                        l2 = l2.union(set(neighbours[k]).intersection(set(index_sensors)) - already_visited)
                        for k2 in n3:
                            M_numbers[i][k2] = d + 1
                            M_list[i][k2] = M_list[i][k] + [k2]
                            M_numbers[k2][i] = d + 1
                            M_list[k2][i] = M_list[i][k] + [k2]
                        for k2 in l2:
                            M_numbers[i][k2] = d
                            M_list[i][k2] = M_list[i][k] #+ [k2]
                            M_numbers[k2][i] = d
                            M_list[k2][i] = M_list[i][k]
                    already_visited = already_visited.union(l)
                    l = l2
                already_visited = already_visited.union(n2)
                n4 = n4.union(n2)
            n = n4
    return (M_numbers,M_list)


def greedy_reparation_com(s,data, M_numbers, M_list):
    """ greedy method to fix the connectivity constraint given matrix calculated before
    """
    M_list = [[set(i) for i in j]for j in M_list]
    reached = s.reached(data)
    sensors = s.get_index_sensors()
    n = s.get_size()
    while len(reached) != s.compute_value() + (1-s.sensors[0]):
        mini = float('inf')
        for i in sensors:
            if i not in reached:
                for j in reached:
                    d = M_numbers[i][j]
                    if d < mini:
                        sensor_to_connect = i
                        sensors_to_add = M_list[i][j]
        for i in sensors_to_add:
            s.add_sensor(i)
            for j in range(n):
                for k in range(n):
                    if M_numbers[j][k] > M_numbers[j][i] + M_numbers[j][k] -1:
                        M_numbers[i][k] = M_numbers[i][j] + M_numbers[j][k] -1
                        M_numbers[k][i] = M_numbers[i][j] + M_numbers[j][k] -1
                        M_list[i][k] = M_list[i][j].union(M_list[j][i])
                        M_list[k][i] = M_list[i][j].union(M_list[j][i])
        reached = s.reached(data)

def kruskal_reparation_com(s,data, M_list, M_numbers):
    """ kruskal use of a minimum spanning tree to fix the connectivity constraint given matrix calculated in self.min_number_capt_to_add
    """
    if s.is_sensor(0):
        size_g = s.compute_value()
        sensors = s.get_index_sensors()
    else :
        size_g = s.compute_value() + 1
        sensors = [0] + s.get_index_sensors()
    adj = np.ones((size_g,size_g), dtype = 'bool')
    for i in range(size_g):
        adj[i][i] = False

    g = Graph(size_g,adjacency = adj,edges_value = np.array([[float(M_numbers[i][j]) for i in sensors] for j in sensors]))
    (adj, ev) = g.kruskal()
    for i in range(size_g):
        for j in range(i+1,size_g):
            if adj[i][j]:
                ind_i = sensors[i]
                ind_j = sensors[j]
                for k in M_list[ind_i][ind_j]:
                    s.add_sensor(k)
    assert s.related(data)


def greedy_solution_detect(data):
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
	return Solution(n, [(i in sensors) for i in range(n)])





if __name__ == '__main__':

    from timeit import default_timer as timer

    # test of the reparation method solution class
    nb_rows = nb_columns = 30
    r_com = 1
    r_sens = 1
    n = nb_columns*nb_rows
    d = Data(r_com, r_sens, nb_rows, nb_columns)
    b = [False for i in range(n)]
    s = greedy_solution_detect(d)
    print("initial value of the greedy constructed and not eligible solution :", s.compute_value())

    # test of the reparation methods
    start = timer()
    (M_numbers, M_list) = min_number_capt_to_add(s,d)
    print("time to construct the matrix :", timer() - start)
    s2 = s.copy()
    start = timer()
    greedy_reparation_com(s2,d, M_numbers, M_list)
    print("time to fix the solution :", timer()- start)
    print("value after the greeedy reparation :", s2.compute_value())

    start = timer()
    kruskal_reparation_com(s,d, M_list, M_numbers)
    print("time to fix the solution :", timer()- start)
    print("value after the kruskal reparation :", s.compute_value())



	
