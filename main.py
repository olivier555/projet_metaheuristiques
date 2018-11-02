# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:36:29 2018

@author: olivi
"""

from initial_path_finder import PathFinder
from data import Data
from visualization import Visualizator
from lower_bound_founder import LowerBoundFounder
from local_search import *
from fusion import Fusion
from search_two_to_one import SearchTwoToOne
from switch import Switch

data = Data(r_com = 2, r_sens = 1, file_name = "Instances/captANOR225_9_20.dat")
#data = Data(r_com = 1, r_sens = 1, nb_rows = 5, nb_columns = 5)


print("Founding solution ...")
path_finder = PathFinder(data)
solution = path_finder.create_path()
initial_value = solution.compute_value()
"""
visualizator = Visualizator(data, solution)

visualizator.print_sensors()
"""

"""
print("Creating visualizations ...")
visualizator = Visualizator(data, solution)

visualizator.print_sensors()
visualizator.print_sensors_com()
visualizator.print_sensors_sens()
"""
print("Local search ...")
remove_targets(solution, data)
new_value = solution.compute_value()

visualizator = Visualizator(data, solution)

visualizator.print_sensors()

print("switch")
switch = Switch(data)
switch.switch_sensors(solution, 5, 4)

visualizator = Visualizator(data, solution)

visualizator.print_sensors()

"""
print("Search two to one ...")
search_two = SearchTwoToOne(data)
search_two.search(solution, 10, 30)

print("Creating visualizations ...")
visualizator = Visualizator(data, solution)

visualizator.print_sensors()
"""
print(new_value)
print(solution.compute_value())
#visualizator.print_sensors_com()
#visualizator.print_sensors_sens()

"""
print("Lower bound ...")
lower_bound_founder = LowerBoundFounder(data)
result = lower_bound_founder.find_lower_bound()
print("Lower bound :", - result.fun)
"""

"""
print("switch")
switch = Switch(data)




print("Initial value: ", initial_value)
print("Value after local search: ", new_value)
for i in range(50):
    switch.switch_sensors(new_solution, 10)
    new_solution = local_search.remove_targets(new_solution, data)
    print("Value after switch and local search: ", new_solution.compute_value())

switch.switch_sensors(new_solution, 10)
"""
"""if new_solution is not None:
    print("Value after 2 to 1 search: ", new_solution.compute_value())"""
"""

initial_solutions = [path_finder.create_path() for i in range(2)]

local_search = LocalSearch()
ls_solutions = [local_search.remove_targets(s, data) for s in initial_solutions]
print("Fusion ...")
fusion = Fusion(data)
new_solution_hor = fusion.fusion_horizontal(ls_solutions[0], ls_solutions[1], 100)

new_solution_ver = fusion.fusion_vertical(ls_solutions[0], ls_solutions[1], 100)

print("Initial value 1: ", initial_solutions[0].compute_value())
print("Initial value 2: ", initial_solutions[1].compute_value())

if new_solution_hor is not None:
    print("New value hor : ", new_solution_hor.compute_value())

if new_solution_ver is not None:
    print("New value ver: ", new_solution_ver.compute_value())"""



