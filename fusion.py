# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 08:48:28 2018

@author: olivi
"""

import numpy as np
import random as rd
from solution import Solution
from local_search import remove_targets

class Fusion:

    def __init__(self, data):
        self.data = data
        self.points_sorted_x = sorted(data.points, key=lambda x: x[1])
        self.index_sorted_x = np.array([self.points_sorted_x.index(v) for v in data.points], int)
        self.points_sorted_y = sorted(data.points, key=lambda x: x[2])
        self.index_sorted_y = np.array([self.points_sorted_y.index(v) for v in data.points], int)
        self.distances_diag = [(0.95 * x[2] + x[1]) / (1 + 0.95 ** 2) for x in data.points]
        self.distances_diag.sort()
        self.points_sorted_diag = sorted(data.points, key=lambda x: (0.95 * x[2] + x[1]) / (1 + 0.95 ** 2))
        self.index_sorted_diag = np.array([self.points_sorted_y.index(v) for v in data.points], int)
        self.n = data.get_size()

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

    def fusion_horizontal_childrens(self, s_1, s_2):
        return self.fusion_childrens(s_1, s_2, self.index_sorted_x, 1)

    def fusion_vertical_childrens(self, s_1, s_2):
        return self.fusion_childrens(s_1, s_2, self.index_sorted_y, 2)

    def fusion_diag_childrens(self, s_1, s_2):
        return self.fusion_childrens(s_1, s_2, self.index_sorted_diag, 3)

    def fusion_childrens(self, s_1, s_2, index_sorted, direction):
        r = []
        compt = 0
        # samp = np.random.binomial(self.n-3, 0.5, 100) + 1
        while compt < 100 and len(r) < 2:
            # i = samp[compt]
            i = rd.randint(1,self.n - 2)
            # while not(s_1.is_sensor(i) or s_2.is_sensor(i)):
            #     i = rd.randint(1, self.n-2)
            # we have two set of vertices separated by the index i.
            # we creat two new solutions by combining the sensors of each set for two different solutions
            child_1 = Solution(self.n, s_1.sensors * (index_sorted <= i) + s_2.sensors * (index_sorted > i)) 
            child_2 = Solution(self.n, s_2.sensors * (index_sorted <= i) + s_1.sensors * (index_sorted > i))
            childrens = [child_1,child_2]
            v_min = min(s_1.value,s_2.value)
            for c in childrens:
                if not(c.eligible(self.data)):
                    if c.value < v_min :
                        # s = set(c.get_index_sensors())
                        self.restore(c, index_sorted, i, direction)
                        # print(set(c.get_index_sensors()) - s)
                        assert c.eligible(self.data)
                        r.append(c)
                else :
                    r.append(c)
            compt+=1
        return r
    
    def restore(self, s, index_sorted, i, direction): #direction vaut 1 ou 2
        if direction == 1:
            center_value = self.points_sorted_x[i][1]
        elif direction == 2:
            center_value = self.points_sorted_y[i][2]
        else:
            center_value = self.distances_diag[i]

        sensors_to_add = [i]
        r = self.data.r_com      
        for d in [-1,1]:
        #in both ways
            j = i
            add_direction = True
            while add_direction and j < self.n and j > 0:
                if direction == 1:
                    add_direction = abs(self.points_sorted_x[j][1]- center_value) < r
                    ind = self.points_sorted_x[j][0]
                elif direction == 2:
                    add_direction = abs(self.points_sorted_y[j][2]- center_value) < r
                    ind = self.points_sorted_y[j][0]
                else:
                    add_direction = abs(self.distances_diag[j] - center_value) < r
                    ind = self.points_sorted_diag[j][0]
                if add_direction :
                    sensors_to_add.append(ind)
                j += d
                # add_direction = (self.data.points[index_sorted[j]][direction] - center_value)**2 < r

        print(len(sensors_to_add))
        for i in sensors_to_add:
            s.add_sensor(i)

        # assert s.eligible(self.data)
        remove_targets(s, self.data)


