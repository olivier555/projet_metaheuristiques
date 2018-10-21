# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:36:29 2018

@author: olivi
"""

from initial_path_finder import PathFinder
from data import Data
from visualization import Visualizator

data = Data(r_com = 2, r_sens = 1, file_name = "Instances/captANOR225_9_20.dat")
path_finder = PathFinder(data)
solution = path_finder.create_path()
visualizator = Visualizator(data, solution)

visualizator.print_sensors()
visualizator.print_sensors_com()
visualizator.print_sensors_sens()
print("Value: ", solution.compute_value())
