# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:03:45 2018

@author: olivi
"""

import numpy as np

# class LocalSearch:

def remove_targets(solution, data):
    M = data.get_matrix_sens()
    nb_sens = np.matmul(M, solution.sensors.astype(int)) >= 2
    sensors = solution.get_index_sensors()
    for s in sensors:
        if (np.extract(M[s], nb_sens)).all():
            solution.remove_sensor(s)
            if not solution.related_removed(data, s):
                solution.add_sensor(s)
            else:
                nb_sens = np.matmul(M, solution.sensors.astype(int)) >= 2
        # return solution
                
            