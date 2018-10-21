# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 18:49:35 2018

@author: olivi
"""

from copy import deepcopy
from solution import Solution
import numpy as np

class PathFinder:

    def __init__(self, data):
        self.data = data

    def create_path(self):
        self.neighbours = []
        self.detected = set([0])
        self.solution = Solution(len(self.data.points))
        self.add_neighbours(0)
        print(self.neighbours)
        while len(self.neighbours) != 0:
            sum_norm = sum([len(n["neighbours_sens"]) for n in self.neighbours])
            neighbour = np.random.choice(self.neighbours,
                                         p = [len(n["neighbours_sens"]) / sum_norm for n in self.neighbours])
            #neighbour = max(self.neighbours, key=lambda x:len(x['neighbours_sens']))
            self.update_neighbours(deepcopy(neighbour))
            self.add_neighbours(neighbour["id"])
            self.solution.add_sensor(neighbour["id"])
        return self.solution

    def add_neighbours(self, target_id):
        for n in self.data.get_neighbours_com(target_id):
            set_sens = set(self.data.get_neighbours_sens(n) + [n])
            set_reduced = set_sens.difference(self.detected)
            if len(set_reduced) != 0:
                self.neighbours.append({"id": n, "neighbours_sens": set_reduced})

    def update_neighbours(self, neighbour_added):
        self.detected = self.detected.union(neighbour_added["neighbours_sens"])
        for n in self.neighbours:
            n["neighbours_sens"] = n["neighbours_sens"].difference(neighbour_added["neighbours_sens"])
        self.neighbours = [n for n in self.neighbours if n["id"] != neighbour_added["id"]
                                                         and len(n["neighbours_sens"]) != 0]
