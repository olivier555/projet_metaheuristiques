# -*- coding: utf-8 -*-
"""
Function to remove useless sensors of a solution
"""

import numpy as np

def remove_targets(solution, data):
    """ remove sensors that are useless for the solution.
    <!> solution must be eligible
    """
    M = data.get_matrix_sens()
    nb_sens = np.matmul(M, solution.sensors.astype(int)) >= 2
    sensors = solution.get_index_sensors()
    np.random.shuffle(sensors)
    for s in sensors:
        if (np.extract(M[s], nb_sens)).all():
            solution.remove_sensor(s)
            if not solution.related_removed(data, s):
                solution.add_sensor(s)
            else:
                nb_sens = np.matmul(M, solution.sensors.astype(int)) >= 2
        # return solution
                
            