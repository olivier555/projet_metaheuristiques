# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 08:48:28 2018

@author: olivi
"""

import numpy as np
from solution import Solution

class Fusion:

    def __init__(self, data):
        self.data = data
        points_sorted_x = sorted(data.points, key=lambda x: x[1])
        self.index_sorted_x = np.array([points_sorted_x.index(v) for v in data.points], int)
        points_sorted_y = sorted(data.points, key=lambda x: x[2])
        self.index_sorted_y = np.array([points_sorted_y.index(v) for v in data.points], int)

    def fusion_horizontal(self, solution_1, solution_2, nb_test):
        return self.fusion(solution_1, solution_2, self.index_sorted_x, nb_test)

    def fusion_vertical(self, solution_1, solution_2, nb_test):
        return self.fusion(solution_1, solution_2, self.index_sorted_y, nb_test)

    def fusion(self, solution_1, solution_2, index_sorted, nb_test):
        old_value = min(solution_1.compute_value(), solution_2.compute_value())
        index = set(range(self.data.get_size() // 2))
        for j in range(min(nb_test, self.data.get_size() // 2)):
            i = index.pop()
            sensors_fusion = solution_1.sensors * (index_sorted <= i) + solution_2.sensors * (index_sorted > i)
            new_solution = Solution(self.data.get_size(), sensors_fusion)
            if new_solution.compute_value() < old_value:
                if new_solution.eligible(self.data):
                    return new_solution
            sensors_fusion_other = solution_2.sensors * (index_sorted <= i) + solution_1.sensors * (index_sorted > i)
            new_other_solution = Solution(self.data.get_size(), sensors_fusion_other)
            if new_other_solution.compute_value() < old_value:
                if new_other_solution.eligible(self.data):
                    return new_other_solution
