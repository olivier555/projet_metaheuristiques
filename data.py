# -*- coding: utf-8 -*-
"""
Class Data with the parameters of the problem,
the position of the targets and the neighbourhood matrix
"""

import numpy as np
from graph import *

class Data:

    def __init__(self, r_com, r_sens, nb_rows = None, nb_columns = None, file_name = None):
        if file_name is not None:
            self.points = self.read_file(file_name)
        elif nb_rows is not None and nb_columns is not None:
            self.points = self.create_grid(nb_rows, nb_columns)
        else:
            raise ValueError('Not enough arguments to define the problem')
        self.n = len(self.points)
        self.r_com = r_com
        self.r_sens = r_sens
        self.create_matrix_distance()
        self.set_matrix_com(self.create_matrix_radius(r_com))
        self.set_graph_com()
        self.set_matrix_sens(self.create_matrix_radius(r_sens))
        self.set_graph_sens()


    def create_grid(self, nb_rows, nb_columns):
        points = []
        for i in range(nb_columns):
            for j in range(nb_rows):
                points.append([i * nb_rows + j, i, j])
        return points
    
    def read_file(self, file_name):
        file = open(file_name, "r")
        text = file.read()
        file.close()
        lines = text.split("\n")
        points = []
        for line in lines:
            new_line = [v.split(" ") for v in line.split(" ") if v != '']
            if len(new_line) != 0:
#                if float(new_line[1][0]) < 4 and float(new_line[2][0]) < 4:
#                    points.append([int(new_line[0][0]),
#                                 float(new_line[1][0]),
#                                 float(new_line[2][0])])
                points.append([int(new_line[0][0]),
                                 float(new_line[1][0]),
                                 float(new_line[2][0])])
        return points

    def create_matrix_distance(self):
        self.distances_2 = np.zeros((self.n, self.n))
        for i in range(self.n):
            self.distances_2[i][i] = 0.0
            for j in range(i+1,self.n):
                distance_x = (self.points[i][1] - self.points[j][1]) ** 2
                distance_y = (self.points[i][2] - self.points[j][2]) ** 2
                self.distances_2[i][j] = distance_x + distance_y
                self.distances_2[j][i] = distance_x + distance_y

    def create_matrix_radius(self, radius):
        matrix = np.zeros((self.n, self.n), dtype = 'bool')
        r = radius ** 2
        matrix = self.distances_2 <= r
        return matrix

    def get_neighbours_com(self, index):
        return self.g_com.get_neighbours(index)

    def get_neighbours_sens(self, index):
        return self.g_sens.get_neighbours(index)

    def set_matrix_com(self, matrix):
        self.matrix_com = matrix

    def get_matrix_com(self):
        return self.matrix_com

    def set_matrix_sens(self, matrix):
        self.matrix_sens = matrix

    def get_matrix_sens(self):
        return self.matrix_sens

    def get_size(self):
        return self.n

    def set_graph_sens(self):
        self.g_sens = Graph(self.n, self.get_matrix_sens(), oriented = False, triangular_sup = False)

    def set_graph_com(self):
        self.g_com = Graph(self.n, self.get_matrix_com(), oriented = False, triangular_sup = False)    

    def get_distance(self, i,j):
        return np.sqrt(self.distances_2[i][j])

    def get_matrix_distance(self):
        return np.sqrt(self.distances_2)