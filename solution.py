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

