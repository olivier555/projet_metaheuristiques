# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:36:29 2018

@author: olivi
"""

from initial_path_finder import PathFinder
from data import Data
from visualization import Visualizator
from lower_bound_founder import LowerBoundFounder

data = Data(r_com = 2, r_sens = 2, file_name = "Instances/captANOR225_9_20.dat")
#data = Data(r_com = 2, r_sens = 1, nb_rows = 10, nb_columns = 10)
print("Founding solution ...")
path_finder = PathFinder(data)
solution = path_finder.create_path()
print("Creating visualizations ...")
visualizator = Visualizator(data, solution)

visualizator.print_sensors()
visualizator.print_sensors_com()
visualizator.print_sensors_sens()

lower_bound_founder = LowerBoundFounder(data)
result = lower_bound_founder.find_lower_bound()
print("Lower bound :", - result.fun)
print("Value: ", solution.compute_value())
