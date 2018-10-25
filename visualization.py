# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 15:34:13 2018

@author: olivi
"""

import matplotlib.pyplot as plt

class Visualizator:

    def __init__(self, data, solution):
        self.data = data
        self.solution = solution

    def print_sensors(self):
        self.print_targets()
        plt.show()

    def print_sensors_com(self):
        for i in range(len(self.data.points)):
            if self.solution.sensors[i] or i == 0:
                for j in self.data.get_neighbours_com(i):
                    if j != i and self.solution.sensors[j]:
                        plt.plot([self.data.points[i][1], self.data.points[j][1]],
                                        [self.data.points[i][2], self.data.points[j][2]],
                                        color = "darkgreen",
                                        linewidth = 0.2
                                        )
        self.print_targets()
        plt.show()

    def print_sensors_sens(self):
        for i in range(len(self.data.points)):
            if self.solution.sensors[i]:
                for j in self.data.get_neighbours_sens(i):
                    if j!=0 and j != i:
                        plt.plot([self.data.points[i][1], self.data.points[j][1]],
                                        [self.data.points[i][2], self.data.points[j][2]],
                                        "--",
                                        color = "darkblue",
                                        linewidth = 0.2
                                        )
        self.print_targets()
        plt.show()

    def print_targets(self):
        sensors_x = [self.data.points[i][1] for i in range(len(self.data.points))
                                            if self.solution.sensors[i] and i != 0]
        sensors_y = [self.data.points[i][2] for i in range(len(self.data.points))
                                            if self.solution.sensors[i] and i != 0]
        no_sensors_x = [self.data.points[i][1] for i in range(len(self.data.points))
                                            if not self.solution.sensors[i] and i != 0]
        no_sensors_y = [self.data.points[i][2] for i in range(len(self.data.points))
                                            if not self.solution.sensors[i] and i != 0]
        plt.scatter(self.data.points[0][1], self.data.points[0][2], c = "black", marker = '^')
        plt.scatter(sensors_x, sensors_y)
        plt.scatter(no_sensors_x, no_sensors_y, c = "black", marker = '+')
