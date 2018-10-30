from timeit import default_timer as timer
import os, sys
from data import Data
from switch import Switch
from search_two_to_one import SearchTwoToOne
from optimize import *
# print(os.path.dirname(sys.argv[0]))
list_data = os.listdir('Instances/')

list_data = [i for i in list_data if i[0:4] == 'capt']
# print(list_data)

d = {}

d[1500] = ['captANOR1500_21_500.dat', 'captANOR1500_15_100.dat']
d[900] = ['captANOR900_15_20.dat']
d[225] = ['captANOR225_9_20.dat']
d[400] = ['captANOR400_10_80.dat']
d[625] = ['captANOR625_15_100.dat']

size_instance = [225,400,625,900,1500]

t_path_finder = {}
t_remove_targets_ini = {}
t_switch_ini = {}
t_remove_targets_two = {}
t_mutation = {}
t_fusion = {}
number_mutation = {}
number_fusion = {}
list_r = [(1,1), (2,1)]
n_population = 20
# nb_switch = [2*i for i in range(1,30)]


#timing of the initial path_finder
for n in size_instance :
	for f in d[n]:
		for (r_com,r_sens) in list_r:
			print("working on instance :", f)
			print("with (r_com,r_sens) =", (r_com,r_sens))
			print(" ")
			solutions = []

			data = Data(r_com = r_com, r_sens = r_sens, file_name = 'Instances/'+ f)
			path_finder = PathFinder(data)
			switch = Switch(data)
			fusioner = Fusion(data)
			search_two = SearchTwoToOne(data)


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


			start = timer()
			for i in range(n_population):
				solutions.append(path_finder.create_path())
			if (n,r_com,r_sens) in t_path_finder:
				t_path_finder[(n,r_com,r_sens)].append((timer() - start)/n_population)
			else :
				t_path_finder[(n,r_com,r_sens)] = [(timer() - start)/n_population]

			#timing of the first remove_targets function
			start = timer()
			for s in solutions:
				remove_targets(s,data)

			if (n,r_com, r_sens) in t_remove_targets_ini:
				t_remove_targets_ini[(n,r_com,r_sens)].append((timer() - start)/n_population)
			else:
				t_remove_targets_ini[(n,r_com,r_sens)] = [(timer() - start)/n_population]

			#timing of the switch_function after the initial path_finder
			start = timer()
			for s in solutions:
				j = rd.randint(0,5 * int(s.value))
				switch.switch_sensors(s, 5, j)
			if (n,r_com, r_sens) in t_switch_ini:
				t_switch_ini[(n,r_com,r_sens)].append((timer() - start)/n_population)
			else:
				t_switch_ini[(n,r_com,r_sens)] = [(timer() - start)/n_population]

			#timing of the first remove_targets function
			start = timer()
			for s in solutions:
				remove_targets(s,data)

			if (n,r_com, r_sens) in t_remove_targets_two:
				t_remove_targets_two[(n,r_com,r_sens)].append((timer() - start)/n_population)
			else:
				t_remove_targets_two[(n,r_com,r_sens)] = [(timer() - start)/n_population]

			[population,best_solution, n_fusion, n_mutation, t_f, t_m] = genetic(solutions, data, mutation, fusion, t_max = 600, timings = True)


			if (n,r_com, r_sens) in number_fusion:
				number_fusion[(n,r_com,r_sens)].append(n_fusion)
			else:
				number_fusion[(n,r_com,r_sens)] = [n_fusion]
			if (n,r_com, r_sens) in number_mutation:
				number_mutation[(n,r_com,r_sens)].append(n_mutation)
			else:
				number_mutation[(n,r_com,r_sens)] = [n_mutation]

			if (n,r_com,r_sens) in t_fusion :
				if n_fusion > 0:
					t_fusion[(n,r_com,r_sens)].append(t_f/n_fusion)
				else:
					t_fusion[(n,r_com,r_sens)].append(None)

			else:
				if n_fusion > 0:
					t_fusion[(n,r_com,r_sens)] = [t_f/n_fusion]
				else:
					t_fusion[(n,r_com,r_sens)] = [None]

			if (n,r_com,r_sens) in t_mutation:
				if n_mutation > 0:
					t_mutation[(n,r_com,r_sens)].append(t_m/n_mutation)
				else:
					t_mutation[(n,r_com,r_sens)].append(None)
			else:
				if n_mutation > 0:
					t_mutation[(n,r_com,r_sens)] = [t_m/n_mutation]
				else :
					t_mutation[(n,r_com,r_sens)] = [None]



print(t_mutation)
print(t_fusion)
print(number_mutation)
print(number_fusion)
print(t_remove_targets_ini)
print(t_path_finder)
print(t_switch_ini)