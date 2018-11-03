# -*- coding: utf-8 -*-
"""
Class that contains a method to replace two sensors by one in an eligible solution
"""

import numpy as np

class SearchTwoToOne:

    def __init__(self, data):
        """ We get the distances between the different targets.
        We fill the lower left triangle by infinity to get only once each couple
        when we do a minimum on this matrix.
        """
        self.data = data
        self.distances =  self.data.get_matrix_distance()
        i_lower = np.tril_indices(len(self.distances), 0)
        self.distances[i_lower] = np.inf

    def search(self, solution, nb_couple, nb_test_couple):
        """ We search to replace couples of sensors by only one sensor.
        We will test to remove nb_couple couples.
        For each couple, we will try to replace them by nb_test_couple different targets.
        """
        # Computing the nb_couple closest couples 
        index_sensors = [i for i in range(len(solution.sensors)) if solution.sensors[i]]
        sub_distances = self.distances[solution.sensors][:, solution.sensors]
        indexes = np.argpartition(sub_distances.flat, min(nb_couple, len(sub_distances.flat) - 1))
        removed = []
        for i in range(min(nb_couple, len(sub_distances.flat))):
            index_min = np.unravel_index(indexes[i], sub_distances.shape)
            # We consider the couple only if none of the sensors has already been removed
            if index_min[0] in removed or index_min[1] in removed:
                continue
            solution.remove_sensor(index_sensors[index_min[0]])
            solution.remove_sensor(index_sensors[index_min[1]])
            common_neighbours = set(self.data.get_neighbours_sens(index_sensors[index_min[0]])).intersection(self.data.get_neighbours_sens(index_sensors[index_min[1]]))
            success = False
            for i in range(min(nb_test_couple, len(common_neighbours))):
                n = common_neighbours.pop()
                # We only consider neighbours that aren't already sensors
                if not solution.is_sensor(n):
                    solution.add_sensor(n)
                    if solution.eligible_two_to_one(self.data, index_sensors[index_min[0]], index_sensors[index_min[1]], n):
                        success = True
                        break
                    solution.remove_sensor(n)
            if not success:
                solution.add_sensor(index_sensors[index_min[0]])
                solution.add_sensor(index_sensors[index_min[1]])
            else:
                removed.append(index_min[0])
                removed.append(index_min[1])
