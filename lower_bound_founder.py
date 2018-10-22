# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:47:49 2018

@author: olivi
"""

from scipy import optimize

class LowerBoundFounder:

    def __init__(self, data):
        self.data = data

    def find_lower_bound(self):
        size = self.data.get_size()
        result = optimize.linprog(c = [- 1] * size,
                                      A_ub = self.data.get_matrix_sens(),
                                      b_ub = [1] * size)
        return result
