# -*- coding: utf-8 -*-
"""
Class that computes eligible solution for the problem.
"""

from copy import deepcopy
from solution import Solution
import numpy as np

class PathFinder:

    def __init__(self, data):
        self.data = data

    def create_path(self):
        """ Create an eligible solution for data.
        We iteratively add sensors connected to the current solution which taps new targets.
        """
        self.neighbours = []
        self.detected = set([0])
        self.solution = Solution(len(self.data.points))
        self.add_neighbours(0)
        while len(self.neighbours) != 0:
            sum_norm = sum([len(n["neighbours_sens"]) for n in self.neighbours])
            proba = [len(n["neighbours_sens"]) / sum_norm for n in self.neighbours]
            neighbour = np.random.choice(self.neighbours, p = proba)
            self.update_neighbours(deepcopy(neighbour))
            self.add_neighbours(neighbour["id"])
            self.solution.add_sensor(neighbour["id"])
        return self.solution

    def add_neighbours(self, target_id):
        """ Update the neighbours list with the neighbours of target_id.
        We add only positions that can tap new targets
        """
        for n in self.data.get_neighbours_com(target_id):
            set_sens = set(self.data.get_neighbours_sens(n) + [n])
            set_reduced = set_sens.difference(self.detected)
            if len(set_reduced) != 0:
                self.neighbours.append({"id": n, "neighbours_sens": set_reduced})

    def update_neighbours(self, neighbour_added):
        """ We update detected targets
        We remove newly taped positions from the list of neighbours for potential sensors.
        """
        self.detected = self.detected.union(neighbour_added["neighbours_sens"])
        for n in self.neighbours:
            n["neighbours_sens"] = n["neighbours_sens"].difference(neighbour_added["neighbours_sens"])
        self.neighbours = [n for n in self.neighbours if n["id"] != neighbour_added["id"]
                                                         and len(n["neighbours_sens"]) != 0]
