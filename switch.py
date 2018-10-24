# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 19:02:45 2018

@author: olivi
"""

class Switch:

    def __init__(self, data):
        self.data = data
        self.nb_neighbours = [len(self.data.get_neighbours_sens(i)) for i in range(self.data.get_size())]

    def switch_sensors(self, solution, nb_test):
        for s in solution.get_index_sensors():
            neighbours_eligible = set([n for n in self.data.get_neighbours_sens(s)
                                         if self.nb_neighbours[n] > self.nb_neighbours[s]
                                         and not solution.sensors[n]])
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
                        