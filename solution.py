"""
This class describes a solution (wihtout considering the data)
"""

import numpy as np

class Solution():

    def __init__(self, n, sensors = None):
        """ We initialize the solution with a boolean list
        or a list of False if no list is provided.
        """
        if sensors is None:
            sensors = np.zeros(n,dtype = 'bool')
        else:
            sensors = np.array(sensors, 'bool')
            assert sensors.size == n, "size of sensors must be equal to n %s"%n
        self.sensors = sensors
        self.value = self.compute_value()
        self.n = n

    def compute_value(self):
        """ Compute the value of the solution.
        It's the value that we try to optimize
        """
        return sum(self.sensors == 1)

    def detected(self, data):
        """ Check if all targets are detected by the solution
        """
        M = data.get_matrix_sens()
        # The sink doesn't have to be detected hence the 1:
        return (np.matmul(M, self.sensors)[1:] >= 1).all()
        # we want all the targets to be detected except the hole


    def reached(self, data):
        """Getting all the sensors that are reachable from the sink.
        """
        index_sensors = set(np.where(self.sensors)[0])
        next_vertex = set(data.get_neighbours_com(0)).intersection(index_sensors)
        reached = {0}.union(next_vertex)
        if 0 in next_vertex:
            next_vertex.remove(0)
        marked = {0}
        while len(next_vertex) > 0 and len(reached) < self.value + (1 - self.sensors[0]):
            index = next_vertex.pop()
            marked.add(index)
            new = set(data.get_neighbours_com(index)).intersection(index_sensors) - marked
            reached = reached.union(new)
            next_vertex = next_vertex.union(new)
        return reached

    def related(self, data):
        """ Check if the current solution is connex.
        The function uses a method of graph traversal starting from the sink.
        """
        reached = self.reached(data)
        return len(reached) == self.value + (1 - self.sensors[0])
        # we want to reach all the sensors from the hole, but we don't want
        # to count the hole twice if it's a sensor

    def related_removed(self, data, id_removed):
        """ A connexity check adapted to the remove_targets function.
        We only check if all the neighbours of id_removed are still connected in the new graph
        <!> The initial solution before the removal must be eligible
        """
        index_sensors = self.get_index_sensors() + [0]
        neighbours_com = list(set(data.get_neighbours_com(id_removed)).intersection(index_sensors))
        set_neighbours = set(neighbours_com)
        first_vertex = neighbours_com[0]
        next_vertex = set(data.get_neighbours_com(first_vertex)).intersection(index_sensors)
        reached = {first_vertex}.union(next_vertex)
        if first_vertex in next_vertex:
            next_vertex.remove(first_vertex)
        marked = {first_vertex}
        while len(next_vertex) > 0 and not set_neighbours.issubset(reached):
            index = next_vertex.pop()
            marked.add(index)
            new = set(data.get_neighbours_com(index)).intersection(index_sensors) - marked
            reached = reached.union(new)
            next_vertex = next_vertex.union(new)
        return set_neighbours.issubset(reached)

    def related_switch(self, data, id_removed, id_add):
        """ A connexity check adapted to the switch class.
        We only check if all the neighbours of id_removed are still connected to id_add in the new graph
        <!> The initial solution before the switch must be eligible
        """
        index_sensors = self.get_index_sensors() + [0]
        set_neighbours = set(data.get_neighbours_com(id_removed)).intersection(index_sensors)
        first_vertex = id_add
        next_vertex = set(data.get_neighbours_com(first_vertex)).intersection(index_sensors + [0])
        reached = {first_vertex}.union(next_vertex)
        if first_vertex in next_vertex:
            next_vertex.remove(first_vertex)
        marked = {first_vertex}
        while len(next_vertex) > 0 and not set_neighbours.issubset(reached):
            index = next_vertex.pop()
            marked.add(index)
            new = set(data.get_neighbours_com(index)).intersection(index_sensors) - marked
            reached = reached.union(new)
            next_vertex = next_vertex.union(new)
        return set_neighbours.issubset(reached)

    def related_two_to_one(self, data, id_removed_1, id_removed_2, id_add):
        """ A connexity check adapted to the search_two_to_one function.
        We only check if all the neighbours of id_removed_1 and id_removed_2
        are connected to id_add in the new graph
        <!> The initial solution before the search must be eligible
        """
        index_sensors = self.get_index_sensors() + [0]
        set_neighbours_1 = set(data.get_neighbours_com(id_removed_1)).intersection(index_sensors)
        set_neighbours_2 = set(data.get_neighbours_com(id_removed_2)).intersection(index_sensors)
        set_neighbours = set_neighbours_1.union(set_neighbours_2)
        first_vertex = id_add
        next_vertex = set(data.get_neighbours_com(first_vertex)).intersection(index_sensors + [0])
        reached = {first_vertex}.union(next_vertex)
        if first_vertex in next_vertex:
            next_vertex.remove(first_vertex)
        marked = {first_vertex}
        while len(next_vertex) > 0 and not set_neighbours.issubset(reached):
            index = next_vertex.pop()
            marked.add(index)
            new = set(data.get_neighbours_com(index)).intersection(index_sensors) - marked
            reached = reached.union(new)
            next_vertex = next_vertex.union(new)
        return set_neighbours.issubset(reached)



    def eligible(self, data):
        """ Check if the solution is eligible.
        """
        return self.detected(data) and self.related(data)

    def eligible_switch(self, data, id_removed, id_add):
        """ Check if the solution is eligible after a switch.
        <!> The initial solution before the switch must be eligible
        """
        return self.detected(data) and self.related_switch(data, id_removed, id_add)

    def eligible_two_to_one(self, data, id_removed_1, id_removed_2, id_add):
        """ Check if the solution is eligible after a search_two_to_one.
        <!> The initial solution before the search must be eligible
        """
        return self.detected(data) and self.related_two_to_one(data, id_removed_1, id_removed_2, id_add)

    def get_size(self):
        return self.n

    def copy(self):
        """ Create a copy of the solution
        """
        s = Solution(self.n, self.sensors.copy())
        return s

    def add_sensor(self, i):
        """ add a sensor and update the value
        """
        if not self.sensors[i]:
            self.sensors[i] = True
            self.value += 1

    def remove_sensor(self, i):
        """ remove a sensor and update the value
        """
        if self.sensors[i]:
            self.sensors[i] = False
            self.value -= 1

    def is_sensor(self, index):
        """ check if there is a sensor at index
        """
        return self.sensors[index]

    def get_index_sensors(self):
        """ get a list of all the sensors in the solution.
        """
        return list(np.where(self.sensors)[0])

    def min_number_capt_to_add(self,data):
        index_sensors = self.get_index_sensors()

        M_list = [[None for j in range(self.n)] for i in range(self.n)]
        M_numbers = [[None for j in range(self.n)] for i in range(self.n)]
        neighbours = [data.get_neighbours_com(i) for i in range(self.n)]
        
        for i in range(self.n):
            already_visited = set([i])
            for j in index_sensors:
                if M_numbers[j][i] != None:
                    M_numbers[i][j] = M_numbers[j][i]
                    M_list[i][j] = M_list[j][i]
                    already_visited.add(j)


            if self.is_sensor(i):
                d = 0
                M_list[i][i] = []
            else : 
                d = 1
                M_list[i][i] = [i]
            M_numbers[i][i] = d
            n = set([i])
            # descente i
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
        return (M_numbers,M_list) #, M_numbers[0], M_list[0])


    def greedy_reparation_com(self,data, M_numbers, M_list):
        M_list = [[set(i) for i in j]for j in M_list]
        reached = self.reached(data)
        sensors = self.get_index_sensors()
        while len(reached) != self.value + (1-self.sensors[0]):
            mini = float('inf')
            for i in sensors:
                if i not in reached:
                    for j in reached:
                        d = M_numbers[i][j]
                        if d < mini:
                            sensor_to_connect = i
                            sensors_to_add = M_list[i][j]
            for i in sensors_to_add:
                self.add_sensor(i)
                for j in range(self.n):
                    for k in range(self.n):
                        if M_numbers[j][k] > M_numbers[j][i] + M_numbers[j][k] -1:
                            M_numbers[i][k] = M_numbers[i][j] + M_numbers[j][k] -1
                            M_numbers[k][i] = M_numbers[i][j] + M_numbers[j][k] -1
                            M_list[i][k] = M_list[i][j].union(M_list[j][i])
                            M_list[k][i] = M_list[i][j].union(M_list[j][i])
            reached = self.reached(data)

    def kruskal_reparation_com(self,data, M_list, M_numbers):
        
        if self.is_sensor(0):
            size_g = self.value
            sensors = self.get_index_sensors()
        else :
            size_g = self.value + 1
            sensors = [0] + self.get_index_sensors()
        adj = np.ones((size_g,size_g),dtype = 'bool')
        for i in range(size_g):
            adj[i][i] = False
        # adj.shape
        # np.array([[M_numbers[i][j] for i in sensors] for j in sensors]).shape)
        g = Graph(size_g,adjacency = adj,edges_value = np.array([[M_numbers[i][j] for i in sensors] for j in sensors]))
        (adj, ev) = g.kruskal()
        for i in range(size_g):
            for j in range(i+1,size_g):
                if adj[i][j]:
                    ind_i = sensors[i]
                    ind_j = sensors[j]
                    for k in M_list[ind_i][ind_j]:
                        self.add_sensor(k)
        assert self.related(data)



if __name__ == '__main__':
    import numpy as np
    from greedy_connect import *
    from data import *
    from timeit import default_timer as timer

    nb_rows = nb_columns = 15
    r_com = 1
    r_sens = 1
    n = nb_columns*nb_rows
    d = Data(r_com, r_sens, nb_rows, nb_columns)
    b = [False for i in range(n)]
    sensors = list(greedy_solution_sens(d))
    for i in sensors:
        b[i] = True
    s = Solution(n,b)
    print(s.compute_value())
    print(s.copy())
    start = timer()
    (M_numbers, M_list) = s.min_number_capt_to_add(d)
    print(timer() - start)

    s2 = s
    start = timer()
    s2.greedy_reparation_com(d, M_numbers, M_list)
    print(timer()- start)
    print(s2.compute_value())

    start = timer()
    s.kruskal_reparation_com(d, M_list, M_numbers)
    print(timer()- start)
    print(s.compute_value())


