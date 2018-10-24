import numpy as np
from timeit import default_timer as timer
import random as rd
from search_two_to_one import SearchTwoToOne
from local_search import remove_targets


def genetic(population, data, mutation, fusion, n_iter = 50, mutation_proba = 0.1, prop_children_kept = 0.3, t_max = 60):
	start = timer()
	t = 0
	n = len(population)
	i = 1
	while i < n_iter and t < t_max:
		print('')
		print("genetic iteration :", i)
		np.random.shuffle(population)
		list_childrens = []
		list_childrens_value = []
		for j in range(int(n/2)):
			childrens = fusion(population[2*j],population[2*j+1])
			for k in range(2):
				p = rd.random()
				assert(childrens[k].eligible(data))
				if p < mutation_proba:
					childrens[k] = mutation(childrens[k])
					# print('mutation done')
					print('hey')
				assert(childrens[k].eligible(data))
			# childrens is a list of two doable solutions 
			list_childrens += childrens
			list_childrens_value += [childrens[0].compute_value(), childrens[1].compute_value()]
		index_best_childrens = np.argsort(list_childrens_value)


		parents_value = [s.compute_value() for s in population]
		index_best_parents = np.argsort(parents_value)

		n_childrens = int(n*prop_children_kept)
		n_parents = n - n_childrens
		population = [population[index_best_parents[i]] for i in range(n_parents)]
		population += [list_childrens[index_best_childrens[i]] for i in range(n_childrens)]
		values_pop = [s.compute_value() for s in population]
		print('minimum initial value...')
		print(min(values_pop))
		t = timer() - start
		i+=1
		for j in population:
			assert j.eligible(data)
	return population


def mutation_1(s,data, p_ajout = 0.1):
	if rd.random() > p_ajout:
		i = rd.randint(0, s.get_size()-1)
		s.add_sensor(i)

	remove_targets(s, data)
	search_two = SearchTwoToOne(data)
	search_two.search(s, 10, 30)

	return s



if __name__ == '__main__':
	from data import *
	from fusion import *
	from initial_path_finder import PathFinder
	

	data = Data(r_com = 2, r_sens = 1, file_name = "Instances/captANOR1500_21_500.dat")
	n_population = 20
	population = []

	
	print('creating initial population...')
	path_finder = PathFinder(data)
	for i in range(n_population):
		solution = path_finder.create_path()
		population.append(solution)

	print('done!')
	values_pop = [s.compute_value() for s in population]
	print('minimum initial value...')
	print(min(values_pop))

	def mutation(s):
		return mutation_1(s,data)

	f = Fusion(data)
	def fusion(s_1,s_2):
		p = rd.random()
		if p < 0.5:
			return f.fusion_vertical_childrens(s_1,s_2)
		else:
			return f.fusion_horizontal_childrens(s_1,s_2)


	population = genetic(population, data, mutation, fusion, n_iter = 60, t_max  = 120)
