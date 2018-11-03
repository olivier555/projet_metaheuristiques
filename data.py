# -*- coding: utf-8 -*-
"""
Class Data with the parameters of the problem,
the position of the targets and the neighbourhood matrix
"""

import numpy as np
from graph import *

class Data:

    def __init__(self, r_com, r_sens, nb_rows = None, nb_columns = None, file_name = None):
        """ We initialize the target points with an insatnce file or
        with a grid with nb_rows and nb_columns.
        We create some matrices that we will use in other part of the code.
        """
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
        """ We create all the points of the grid.
        """
        points = []
        for i in range(nb_columns):
            for j in range(nb_rows):
                points.append([i * nb_rows + j, i, j])
        return points
    
    def read_file(self, file_name):
        """ We read the points from the instance file.
        """
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

    def create_matrix_distance(self):
        """ We compute all the distance between 2 targets.
        We store the results inside a numpy array.
        """
        self.distances_2 = np.zeros((self.n, self.n))
        for i in range(self.n):
            self.distances_2[i][i] = 0.0
            for j in range(i+1,self.n):
                distance_x = (self.points[i][1] - self.points[j][1]) ** 2
                distance_y = (self.points[i][2] - self.points[j][2]) ** 2
                self.distances_2[i][j] = distance_x + distance_y
                self.distances_2[j][i] = distance_x + distance_y

    def create_matrix_radius(self, radius):
        """ We compute a binary matrix.
        The coefficient (i, j) is True if the targets i and j are closer than radius.
        """
        matrix = np.zeros((self.n, self.n), dtype = 'bool')
        r = radius ** 2
        matrix = self.distances_2 <= r
        return matrix

    def get_neighbours_com(self, index):
        """ Return the neighbours in communication of the target index.
        """
        return self.g_com.get_neighbours(index)

    def get_neighbours_sens(self, index):
        """ Return the neighbours in captation of the target index.
        """
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
        """ Return the number of points.
        """
        return self.n

    def set_graph_sens(self):
        """ Create the captation graph thanks to matrix_sens
        """        
        self.g_sens = Graph(self.n, self.get_matrix_sens(), oriented = False, triangular_sup = False)

    def set_graph_com(self):
        """ Create the communication graph thanks to matrix_com
        """        
        self.g_com = Graph(self.n, self.get_matrix_com(), oriented = False, triangular_sup = False)    

    def get_distance(self, i,j):
        return np.sqrt(self.distances_2[i][j])

    def get_matrix_distance(self):
        return np.sqrt(self.distances_2)