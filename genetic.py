import numpy as np
from timeit import default_timer as timer
import random as rd
from search_two_to_one import SearchTwoToOne
from local_search import remove_targets


def genetic(population, data, mutation, fusion, n_iter = 50, mutation_proba = 0.4, prop_children_kept = 0.7, t_max = 60, timings = False):
	start = timer()
	t = 0
	n = len(population)
	i = 1
	values_pop = [s.value for s in population]
	best_sol = population[np.argmin(values_pop)]
	best = best_sol.value
	while i < n_iter and t < t_max:
		# print('')
		# print("genetic iteration :", i)
		np.random.shuffle(population)
		list_childrens = []
		list_childrens_value = []
		if timings :
			t_f = 0
			t_m = 0
			n_mutation = 0
			n_fusion = 0
		for j in range(int(n/2)):
			if timings :
				start_f = timer()
				childrens = fusion(population[2*j],population[2*j+1])
				t_f += timer() - start_f
				n_fusion += 1
			else:
				childrens = fusion(population[2*j],population[2*j+1])

			# for c in childrens:
			# 	p = rd.random()
				# assert(childrens[k].eligible(data))
				# if p < mutation_proba:
				# 	start_m = timer()
				# 	c = mutation(c)
				# 	t_m += timer() - start_m
					# print('mutation done')
				# assert(childrens[k].eligible(data))
			# childrens is a list of two doable solutions 
			list_childrens += childrens
			list_childrens_value += [c.compute_value() for c in childrens]
		index_best_childrens = np.argsort(list_childrens_value)


		parents_value = [s.compute_value() for s in population]
		index_best_parents = np.argsort(parents_value)

		n_childrens = min(int(n*prop_children_kept),len(list_childrens))
		# print('n_childrens :', n_childrens)
		n_parents = n - n_childrens
		population = [population[index_best_parents[i]] for i in range(n_parents)]
		population += [list_childrens[index_best_childrens[i]] for i in range(n_childrens)]
		values_pop = [s.compute_value() for s in population]
		best_actual = min(values_pop)
		if best_actual < best:
			best_sol = population[np.argmin(values_pop)]
			best = best_actual
		for c in population:
			p = rd.random()
			if p < mutation_proba:
				if timings:
					start_m = timer()
					c = mutation(c)
					t_m += timer() - start_m
				else:
					c = mutation(c)
					n_mutation += 1


		values_pop = [s.compute_value() for s in population]
		# print('minimum value...')
		# print(min(values_pop))
		t = timer() - start
		i+=1
		# for j in population:
		# 	assert j.eligible(data)

		# print('time fusion :',t_f)
		# print('time mutation :', t_m)
	if timings :
		return [population,best_sol, n_fusion, n_mutation, t_f, t_m]
	else:
		return[population,best_sol]



def mutation_1(s,data, switch, search_two, p_ajout = 0.5):
	while rd.random() < p_ajout:
		i = rd.randint(0, s.get_size()-1)
		s.add_sensor(i)




	# assert(s.eligible(data))
	# remove_targets(s, data)
	# assert s.eligible(data)
	# search_two = SearchTwoToOne(data)
	j = rd.randint(1,int(s.value/5))
	switch.switch_sensors(s,5,j)#int(s.value/10))
	search_two.search(s, 10, 30)

	remove_targets(s,data)
	# assert s.eligible(data)
	return s



if __name__ == '__main__':
	from data import *
	from fusion import *
	from initial_path_finder import PathFinder
	from switch import Switch

	# data = Data(r_com = 2, r_sens = 1, file_name = "Instances/captANOR625_15_100.dat")
	data = Data(r_com = 1, r_sens = 1, nb_rows = 15, nb_columns = 15)
	n_population = 50
	population = []

	switch = Switch(data)
	print('creating initial population...')
	path_finder = PathFinder(data)
	for i in range(n_population):
		solution = path_finder.create_path()
		remove_targets(solution,data)
		j = rd.randint(0, 5*int(solution.value))
		switch.switch_sensors(solution, 5, j)
		remove_targets(solution,data)
		population.append(solution)

	print('done!')
	values_pop = [s.compute_value() for s in population]
	print('minimum initial value...')
	print(min(values_pop))

	search_two = SearchTwoToOne(data)
	def mutation(s):
		return mutation_1(s, data, switch, search_two)

	f = Fusion(data)
	def fusion(s_1,s_2):
		p = rd.random()
		if p < 0.5:
			return f.fusion_vertical_childrens(s_1,s_2)
		else:
			return f.fusion_horizontal_childrens(s_1,s_2)


	[population,best_solution] = genetic(population, data, mutation, fusion, n_iter = 10000, t_max  = 300)
	
	print(best_solution.value)
	switch.switch_sensors(best_solution, 100, 100)
	search_two.search(best_solution, 100, 20)
	print(best_solution.value)



	from visualization import *
	v = Visualizator(data,best_solution)
	v.print_sensors()
	v.print_sensors_com()
	v.print_sensors_sens()