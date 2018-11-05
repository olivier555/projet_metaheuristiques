# -*- coding: utf-8 -*-
"""
Function optimize to launch the entire algorithm on some data with all parameters
"""

from genetic import *
from data import *
from fusion import *
from initial_path_finder import PathFinder
from switch import Switch
import random as rd
from timeit import default_timer as timer
from visualization import Visualizator

def create_initial_population(data, nb_population, switch):
    """ We create the initial population.
    We get those solutions with path_finder then we improve them
    thanks to remove_targets and switch.
    """
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
    """ We make a last search for the best solution to be sure
    to be in local optima for our neighbourhoods
    """
    remove_targets(solution, data)
    search_two.search(solution, solution.value, solution.value)
    switch.switch_sensors(solution, solution.value, solution.value)
    remove_targets(solution, data)
    search_two.search(solution, solution.value, solution.value)

def optimize(data, nb_population, nb_iter_max, t_max, p_mutation_min, p_mutation_max, prop_children_kept, stagnancy_max):
    """ Function which launch our heuristic for data and return the best solution found
    """
    start = timer()
    # Initialization of the different classes used
    switch = Switch(data)
    search_two = SearchTwoToOne(data)
    fusioner = Fusion(data)
    def mutation(s, increase_factor):
        """ We call the mutation function defined in genetic.py
        """
        return mutation_1(s, data, switch, search_two, increase_factor)
    def fusion(s_1,s_2):
        """ Function that fusion two solutions.
        We do equiprobably an horizontal, vertical or diagonal fusion
        """
        p = rd.randint(0, 3)
        if p == 0:
            return fusioner.fusion_vertical_childrens(s_1,s_2)
        elif p == 1:
            return fusioner.fusion_horizontal_childrens(s_1,s_2)
        else:
            return fusioner.fusion_diag_childrens(s_1, s_2)
    initial_population = create_initial_population(data, nb_population, switch)
    t_creation = (timer() - start)
    assert(t_max - (timer() - start) > 0)
    [population, best_solution, t_best] = genetic(population = initial_population,
                                                  data = data,
                                                  mutation = mutation,
                                                  fusion = fusion,
                                                  n_iter = nb_iter_max,
                                                  mutation_proba_min = p_mutation_min,
                                                  mutation_proba_max = p_mutation_max,
                                                  prop_children_kept = prop_children_kept,
                                                  t_max = t_max - (timer() - start),
                                                  stagnancy_max = stagnancy_max)
    treat_best_solution(best_solution, data, switch, search_two)
    t_total = t_creation + t_best
    return best_solution

if __name__ == '__main__':

#    data = Data(r_com = 2, r_sens = 1, file_name = "Instances/captANOR1500_21_500.dat")
    data = Data(r_com = 1, r_sens = 1, nb_rows = 15, nb_columns = 15)
    nb_population = 30
    nb_iter_max = 10
    t_max = 90
    p_mutation_min = 0.3
    p_mutation_max = 0.6
    prop_children_kept = 0.8
    stagnancy_max = 20

    solution = optimize(data, nb_population, nb_iter_max, t_max, p_mutation_min, p_mutation_max, prop_children_kept, stagnancy_max = stagnancy_max)
    visualizator = Visualizator(data, solution)

    visualizator.print_sensors()