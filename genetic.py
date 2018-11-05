# -*- coding: utf-8 -*-
"""
File with the function of the genetic algorithm.
"""

import numpy as np
from timeit import default_timer as timer
import random as rd
from search_two_to_one import SearchTwoToOne
from local_search import remove_targets

def genetic(population, data, mutation, fusion, n_iter = 50, mutation_proba_min = 0.4, mutation_proba_max = 0.6, prop_children_kept = 0.7, t_max = 60, stagnancy_max = 0, timings = False, inc = True):
    """ Function for the genetic algorithm.
    parameters:
        -population: initial population
        -data: structure of the problem (points, r_com, r_sens, matrices)
        -mutation: function used for the mutation of a solution
        -fusion: function used to fusion 2 solutions
        -n_iter: maximum number of iterations in the genetic algorithm
        -mutation_proba_min, mutation_proba_max: probability for a solution to have
        a mutation at each iteration. It the solution aren't improving for several iterations,
        the probability increase from mutation_proba_min to mutation_proba_max
        -prop_children_kept: at each iteration we keep at most this proportion
        of the best children created. The population is completed with the best parents.
        -t_max: maximum time of running
        -stagnancy_max: We stop the algorithm only if there is more than stagnancy_max
        iterations without improvement. 
        <!> t_max and n_iter can be surpassed if stagnancy_max!= 0
        -timings: boolean indicating if we compute different times for testing.
    """
    start = timer()
    t = 0
    n = len(population)
    i = 1
    values_pop = [s.compute_value() for s in population]
    best_sol = population[np.argmin(values_pop)]
    best = best_sol.value
    n_stagnancy = 0
    while (i <= n_iter and t < t_max) or n_stagnancy < stagnancy_max:
        print("genetic iteration :", i)
        # Creation of children by fusion of solutions
        np.random.shuffle(population)
        list_childrens = []
        list_childrens_value = []
        if timings :
            t_f = 0
            t_m = 0
            n_mutation = 0
            n_fusion = 0
        for j in range(int(n / 2)):
            if timings :
                start_f = timer()
                childrens = fusion(population[2 * j], population[2 * j + 1])
                t_f += timer() - start_f
                n_fusion += 1
            else:
                childrens = fusion(population[2 * j], population[2 * j + 1])

            list_childrens += childrens
            list_childrens_value += [c.value for c in childrens]

        # Selection of the best children and parents
        index_best_childrens = np.argsort(list_childrens_value)
        parents_value = [s.value for s in population]
        index_best_parents = np.argsort(parents_value)
        n_childrens = min(int(n*prop_children_kept),len(list_childrens))
        n_parents = n - n_childrens
        population = [population[index_best_parents[i]] for i in range(n_parents)]
        population += [list_childrens[index_best_childrens[i]] for i in range(n_childrens)]

        # Compute current best solution
        best_actual = min(population[0].value, population[n_parents].value)
        if best_actual < best:
            if population[0].value < population[n_parents].value:
                best_sol = population[0].copy()
                print('better solution in the parents')
            else:
                best_sol = population[n_parents].copy()
                print('better solution after a fusion')
            best = best_actual
            n_stagnancy = 0
        else:
            n_stagnancy += 1

        # Mutate solution with a probability mutation_proba
        mutation_proba = min(mutation_proba_max, mutation_proba_min + (n_stagnancy / 10) * (mutation_proba_max - mutation_proba_min))
        for c in population:
            p = rd.random()
            if p < mutation_proba:
                # The mutations become more important when increase_factor is big
                if n_stagnancy > 10 and inc:
                    increase_factor = min((n_stagnancy - 10), 10)
                else:
                    increase_factor = 1
                if timings:
                    start_m = timer()
                    impr = True
                    v = c.compute_value()
                    while impr: 
                        c = mutation(c, increase_factor)
                        n_mutation += 1
                        impr = (c.compute_value() < v - 0.001)
                        v = c.compute_value()
                    t_m += timer() - start_m
                else:
                    impr = True
                    v = c.compute_value()
                    while impr: 
                        c = mutation(c, increase_factor)
                        impr = (c.compute_value() < v - 0.001)
                        v = c.compute_value()


        print("Best value: ", best)
        t = timer() - start
        i += 1

    values_pop = [s.compute_value() for s in population]
    if min(values_pop) < best: #improvement in the last mutations
        best = min(values_pop)
        best_sol = population[np.argmin(values_pop)].copy()
    if timings :
        return [population,best_sol, n_fusion, n_mutation, t_f, t_m, i]
    else:
        return[population,best_sol]


def mutation_1(s,data, switch, search_two, increase_factor = 1, p_ajout = 0.5):
    """ The mutation function used for the genetic algorithm.
    It randomly adds some sensors then explore differnet neighbourhoods
    with switch, search two and remove targets
    """
    while rd.random() < p_ajout:
        i = rd.randint(0, s.get_size() - 1)
        s.add_sensor(i)

    j = rd.randint(1, int(s.compute_value() / 5))
    # The bigger increase_factor is, the more sensors are switched
    switch.switch_sensors(s, 5, j * increase_factor) 
    # The bigger increase_factor is, the more couples we try to replace
    search_two.search(s, 10 * increase_factor, 30)

    remove_targets(s,data)
    return s
