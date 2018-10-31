# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:57:24 2018

@author: olivi
"""

import numpy as np

class SearchTwoToOne:

    def __init__(self, data):
        self.data = data
        self.distances =  self.data.get_matrix_distance()
        i_lower = np.tril_indices(len(self.distances), 0)
        self.distances[i_lower] = np.inf

    def search(self, solution, nb_couple, nb_test_couple):
        index_sensors = [i for i in range(len(solution.sensors)) if solution.sensors[i]]
        sub_distances = self.distances[solution.sensors][:, solution.sensors]
        indexes = np.argpartition(sub_distances.flat, min(nb_couple, len(sub_distances.flat) - 1))
        for i in range(min(nb_couple, len(sub_distances.flat))):
            index_min = np.unravel_index(indexes[i], sub_distances.shape)
            solution.remove_sensor(index_sensors[index_min[0]])
            solution.remove_sensor(index_sensors[index_min[1]])
            common_neighbours = set(self.data.get_neighbours_sens(index_sensors[index_min[0]])
                                  + self.data.get_neighbours_sens(index_sensors[index_min[1]]))
            for i in range(min(nb_test_couple, len(common_neighbours))):
                n = common_neighbours.pop()
                if not solution.is_sensor(n):
                    solution.add_sensor(n)
                    if solution.eligible_two_to_one(self.data, index_sensors[index_min[0]], index_sensors[index_min[1]], n):
                        break
                    solution.remove_sensor(n)
            solution.add_sensor(index_sensors[index_min[0]])
            solution.add_sensor(index_sensors[index_min[1]])
