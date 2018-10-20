# -*- coding: utf-8 -*-
"""
Class Data with the parameters of the problem,
the position of the targets and the neighbourhood matrix
"""

import numpy as np

class Data:

    def __init__(self, file_name, r_com, r_sens):
        self.points = self.read_file(file_name)
        self.r_com = r_com
        self.r_sens = r_sens
        self.set_matrix_com(self.create_matrix_radius(r_com))
        self.set_matrix_sens(self.create_matrix_radius(r_sens))
        

    def __init__(self, nb_rows, nb_columns, r_com, r_sens):
        self.points = self.create_grid(nb_rows, nb_columns)
        self.r_com = r_com
        self.r_sens = r_sens
        self.set_matrix_com(self.create_matrix_radius(r_com))
        self.set_matrix_sens(self.create_matrix_radius(r_sens))

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
                points.append([int(new_line[0][0]),
                             float(new_line[1][0]),
                             float(new_line[2][0])])
        return points

    def create_matrix_radius(self, radius):
        matrix = np.zeros((len(self.points), len(self.points)), dtype = 'bool')
        for i in range(len(self.points)):
            matrix[i][i] = 1
            for j in range(i + 1, len(self.points)):
                distance_x = (self.points[i][1] - self.points[j][1]) ** 2
                distance_y = (self.points[i][2] - self.points[j][2]) ** 2
                if distance_x + distance_y <= radius ** 2:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix

    def get_neighbours_com(self, index):
        return [j for j in range(len(self.points)) if self.matrix_com[index][j]
                                                      and j != index]

    def get_neighbours_sens(self, index):
        return [j for j in range(len(self.points)) if self.matrix_sens[index][j]
                                                      and j != index]

    def set_matrix_com(self, matrix):
        self.matrix_com = matrix

    def get_matrix_com(self):
        return self.matrix_com

    def set_matrix_sens(self, matrix):
        self.matrix_sens = matrix

    def get_matrix_sens(self):
        return self.matrix_sens
