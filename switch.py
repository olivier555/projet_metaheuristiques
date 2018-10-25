# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 19:02:45 2018

@author: olivi
"""
import random

class Switch:

    def __init__(self, data):
        self.data = data
        self.nb_neighbours = [len(self.data.get_neighbours_sens(i)) for i in range(self.data.get_size())]

    def switch_sensors(self, solution, nb_test, nb_to_switch):
        sensors = solution.get_index_sensors()
    # while nb_to_switch > 0: 
        switch_iteration = min(len(sensors),nb_to_switch)
        # nb_to_switch = nb_to_switch - switch_iteration 

        sensors = random.sample(sensors, switch_iteration)
        for s in sensors:
            nb_neighbours = self.nb_neighbours[s]
            neighbours_eligible = []
            for n in self.data.get_neighbours_sens(s):
                if self.nb_neighbours[n] > nb_neighbours and not solution.is_sensor(n):
                    neighbours_eligible.append(n)
            
            sample = random.sample(neighbours_eligible,min(len(neighbours_eligible),nb_test))
            if len(neighbours_eligible) > 0:
                modified = False
                solution.remove_sensor(s)
                for c in range(min(len(neighbours_eligible), nb_test)):
                    new_s = neighbours_eligible.pop()
                    solution.add_sensor(new_s)
                    if solution.eligible(self.data):
                        modified = True
                        break
                    solution.remove_sensor(new_s)
                if not modified:
                    solution.add_sensor(s)
                        