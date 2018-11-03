# -*- coding: utf-8 -*-
"""
Class to find a lower bound of the problem
"""

from scipy import optimize

class LowerBoundFounder:

    def __init__(self, data):
        self.data = data

    def find_lower_bound(self):
        """ Compute the optimal value of the relaxed dual problem
        for the problem without communication constraints
        """
        size = self.data.get_size()
        result = optimize.linprog(c = [- 1] * size,
                                      A_ub = self.data.get_matrix_sens(),
                                      b_ub = [1] * size)
        return result
