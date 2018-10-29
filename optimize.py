# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:05:55 2018

@author: olivi
"""

from genetic import *
from data import *
from fusion import *
from initial_path_finder import PathFinder
from switch import Switch
import random as rd

def create_initial_population(data, nb_population, switch):
    population = []
    path_finder = PathFinder(data)
    for i in range(nb_population):
        solution = path_finder.create_path()
        remove_targets(solution,data)
        j = rd.randint(0,5 * int(solution.value))
        switch.switch_sensors(solution, 5, j)
        remove_targets(solution,data)
        population.append(solution)
    return population

def treat_best_solution(solution, data, switch, search_two):
    remove_targets(solution, data)
    search_two.search(solution, solution.value, solution.value)
    switch.switch_sensors(solution, solution.value, solution.value)
    remove_targets(solution, data)
    search_two.search(solution, solution.value, solution.value)

def optimize(data, nb_population, nb_iter_max, t_max, p_mutation, prop_children_kept):
    switch = Switch(data)
    search_two = SearchTwoToOne(data)
    fusioner = Fusion(data)
    def mutation(s):
        return mutation_1(s, data, switch, search_two)
    def fusion(s_1,s_2):
        p = rd.random()
        if p < 0.33:
            return fusioner.fusion_vertical_childrens(s_1,s_2)
        elif p < 0.67:
            return fusioner.fusion_horizontal_childrens(s_1,s_2)
        else:
            return fusioner.fusion_diag_childrens(s_1, s_2)
    initial_population = create_initial_population(data, nb_population, switch)
    [population,best_solution] = genetic(initial_population, data, mutation, fusion, nb_iter_max, p_mutation, prop_children_kept, t_max)
    treat_best_solution(best_solution, data, switch, search_two)
    return best_solution

if __name__ == '__main__':

    # data = Data(r_com = 2, r_sens = 1, file_name = "Instances/captANOR625_15_100.dat")
    data = Data(r_com = 1, r_sens = 1, nb_rows = 15, nb_columns = 15)
    nb_population = 20
    nb_iter_max = 1000
    t_max = 20
    p_mutation = 0.3
    prop_children_kept = 0.8

    solution = optimize(data, nb_population, nb_iter_max, t_max, p_mutation, prop_children_kept)
