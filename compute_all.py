import pandas as pd
import numpy as np
from data import Data
from optimize import optimize


df = pd.read_csv('Instances/bound.csv')
print(df)


dic_solution =  {}
fails = []
for index, row in df.iterrows():
	data = Data(r_com = row['R_com'], r_sens = row['R_capt'], file_name = "Instances/" + row['instance'])
	nb_population = 30
	nb_iter_max = 500
	t_max = 900 # 15 minutes
	p_mutation_min = 0.3
	p_mutation_max = 0.6
	prop_children_kept = 0.8
	stagnancy_max = 6

	bound = row['bound']
	try:
		# solution = optimize(data, nb_population, nb_iter_max, t_max, p_mutation_min, p_mutation_max, prop_children_kept, stagnancy_max = stagnancy_max)
		dic_solution[(row['instance'],row['R_com'],row['R_capt'])] = ['temps','valeur', 'capteurs', 'n_iteration', 'taille_pop']
	except:
		fails.append(row)


print(fails)

df2 = pd.DataFrame.from_dict(dic_solution, orient = 'index')
df2 = pd.DataFrame.from_dict(dic_solution, orient = 'index')
df2 = pd.DataFrame.from_dict(dic_solution, orient = 'index')
print(df2)
name_output = 'solutions_value.csv'
df2.to_csv(name_output)

