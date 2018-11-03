# -*- coding: utf-8 -*-
"""
Class that switch sensors in an eligible solution
"""
import random

class Switch:

    def __init__(self, data):
        """ We compute the numbers of detection neighbours for each target
        """
        self.data = data
        self.nb_neighbours = [len(self.data.get_neighbours_sens(i)) for i in range(self.data.get_size())]

    def switch_sensors(self, solution, nb_test, nb_to_switch):
        """ We switch sensors in solution.
        We try to switch nb_to_switch sensors.
        For each one, we try to replace it by nb_test of its neighbours.
        We try to replace them only by neighbours that have more detection neighbours than them
        """
        # We get the sensors to switch
        sensors = solution.get_index_sensors()
        switch_iteration = min(len(sensors), nb_to_switch)
        sensors = random.sample(sensors, switch_iteration)

        for s in sensors:
            nb_neighbours = self.nb_neighbours[s]
            neighbours_eligible = []
            # We get the neighbours with more detection neighbours
            for n in self.data.get_neighbours_sens(s):
                if self.nb_neighbours[n] >= nb_neighbours and not solution.is_sensor(n):
                    neighbours_eligible.append(n)
            
            if len(neighbours_eligible) > 0:
                sample = random.sample(neighbours_eligible,min(len(neighbours_eligible),nb_test))
                modified = False
                solution.remove_sensor(s)
                for new_s in sample:
                    solution.add_sensor(new_s)
                    if solution.eligible_switch(self.data, s, new_s):
                        modified = True
                        break
                    solution.remove_sensor(new_s)
                if not modified:
                    solution.add_sensor(s)
                        