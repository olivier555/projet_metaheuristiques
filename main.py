# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:36:29 2018

@author: olivi
"""

from initial_path_finder import PathFinder
from data import Data
from visualization import Visualizator
from lower_bound_founder import LowerBoundFounder
from local_search import LocalSearch

#data = Data(r_com = 2, r_sens = 2, file_name = "Instances/captANOR225_9_20.dat")
data = Data(r_com = 2, r_sens = 1, nb_rows = 5, nb_columns = 5)
print("Founding solution ...")
path_finder = PathFinder(data)
solution = path_finder.create_path()
initial_value = solution.compute_value()
print("Creating visualizations ...")
visualizator = Visualizator(data, solution)

visualizator.print_sensors()
visualizator.print_sensors_com()
visualizator.print_sensors_sens()

local_search = LocalSearch()
new_solution = local_search.remove_targets(solution, data)
new_value = solution.compute_value()

print("Creating visualizations ...")
visualizator = Visualizator(data, new_solution)

visualizator.print_sensors()
visualizator.print_sensors_com()
visualizator.print_sensors_sens()

lower_bound_founder = LowerBoundFounder(data)
result = lower_bound_founder.find_lower_bound()
print("Lower bound :", - result.fun)
print("Initial value: ", initial_value)
print("Value after local search: ", new_value)

