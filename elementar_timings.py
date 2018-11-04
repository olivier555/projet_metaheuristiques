from timeit import default_timer as timer
import os, sys
from data import Data
from switch import Switch
from search_two_to_one import SearchTwoToOne
from optimize import *
import pandas as pd


# This script computes the elementar timings for the instances given in the folder 'Instances/'

list_data = os.listdir('Instances/')
list_data = [i for i in list_data if i[0:4] == 'capt']
d = {}

d[1500] = 'captANOR1500_21_500.dat'# 'captANOR1500_15_100.dat']
d[900] = 'captANOR900_15_20.dat'
d[225] = 'captANOR225_9_20.dat'
d[400] = 'captANOR400_10_80.dat'
d[625] = 'captANOR625_15_100.dat'

size_instance = [225,400,625,900,1500]

# We use dictionnaries for the elementar timings
# Mean time to create a solution with path_finder
t_path_finder = {}
# Mean time to remove targets of a solution created by path_finder
t_remove_targets_ini = {}
# Mean time to do the switch for an initial solution after path_finder and remove_targets_ini
t_switch_ini = {}
# Mean time to try to remove target again after the swithc for an initial solution
t_remove_targets_two = {}
# Mean time needed for one mutation
t_mutation = {}
# Mena time needed for one fusion
t_fusion = {}
number_mutation = {}
number_fusion = {}
list_r = [(1,1), (2,1),(2,2),(3,2)]
n_population = 50

for n in size_instance :
	f = d[n]
	for (r_com,r_sens) in list_r:
		print(" ")
		print("working on instance :", f)
		print("with (r_com,r_sens) =", (r_com,r_sens))
		solutions = []

		data = Data(r_com = r_com, r_sens = r_sens, file_name = 'Instances/'+ f)
		path_finder = PathFinder(data)
		switch = Switch(data)
		fusioner = Fusion(data)
		search_two = SearchTwoToOne(data)


		def mutation(s, increase_factor):
			return mutation_1(s, data, switch, search_two, increase_factor)
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
		t_path_finder[(n,r_com,r_sens)] = (timer() - start)/n_population

		#timing of the first remove_targets function
		start = timer()
		for s in solutions:
			remove_targets(s,data)
		t_remove_targets_ini[(n,r_com,r_sens)] = (timer() - start)/n_population

		#timing of the switch_function after the initial path_finder
		start = timer()
		for s in solutions:
			j = rd.randint(0,5 * int(s.value))
			switch.switch_sensors(s, 5, j)
		t_switch_ini[(n,r_com,r_sens)] = (timer() - start)/n_population

		#timing of the first remove_targets function
		start = timer()
		for s in solutions:
			remove_targets(s,data)
		t_remove_targets_two[(n,r_com,r_sens)] = (timer() - start)/n_population

		[population,best_solution, n_fusion, n_mutation, t_f, t_m, n_iter] = genetic(solutions, data, mutation, fusion, n_iter = 30, t_max = 120, timings = True)

		number_fusion[(n,r_com,r_sens)] = n_fusion
		number_mutation[(n,r_com,r_sens)] = n_mutation

		# update the mean duration of a fusion
		if n_fusion > 0:
			t_fusion[(n,r_com,r_sens)] = t_f/n_fusion
		else:
			t_fusion[(n,r_com,r_sens)] = None

		# update the mean duration of a mutation
		if n_mutation > 0:
			t_mutation[(n,r_com,r_sens)] = t_m/n_mutation
		else :
			t_mutation[(n,r_com,r_sens)] = None


# save everything in a pandas dataframe and then in a csv file
NAME_CSV = 'timings.csv' 
df = pd.DataFrame.from_dict(t_mutation, orient='index', columns = ['t_mutation'])
df.index.name = 'n,r_com,r_sens'
df['t_fusion'] = pd.Series(t_fusion)
df['number_fusion'] = pd.Series(number_mutation)
df['number_mutation'] = pd.Series(number_fusion)
df['t_remove_targets_ini'] = pd.Series(t_remove_targets_ini)
df['t_path_finder'] = pd.Series(t_path_finder)
df['t_switch_ini'] = pd.Series(t_switch_ini)
df['t_remove_targets_two'] = pd.Series(t_remove_targets_two)
df.to_csv(NAME_CSV)