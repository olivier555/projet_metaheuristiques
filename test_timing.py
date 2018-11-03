import pandas as pd 
import matplotlib.pyplot as plt
import re
import numpy as np
from optimize import *
from data import Data
from timeit import default_timer as timer



def list_from_str(s):
	if isinstance(s, str):
		s = re.sub('[(]', '', s)
		s = re.sub('[\[]', '', s)
		s = re.sub('[\]]','',s)
		# print(s)
		s = re.sub('[)]', '', s)
		s = s.split(',')
		s = [float(i) for i in s]
		return s
	else:
		return [s]




def clean_df(filename):
	df = pd.read_csv(filename)
	df['n,r_com,r_sens'] = df['n,r_com,r_sens'].apply(lambda x: list_from_str(x))
	df['n'] = df['n,r_com,r_sens'].apply(lambda x: x[0])
	df['r_com'] = df['n,r_com,r_sens'].apply(lambda x: x[1])
	df['r_sens'] = df['n,r_com,r_sens'].apply(lambda x: x[2])
	df.drop('n,r_com,r_sens', axis = 1, inplace = True)
	return df

# this function computes the size of the population to use the metaheuristic
# with less tant T_ini seconds to compute the initial population and less than T seconds
# for the entire metaheuristic with at least n_iterations iterations, and a probability of 
# mutation p_m
# The datas are n points, and radiuses (r_com, r_sens) for communication and detection
# We also use the dataframe df with our previous computations of the elementar timings 
def size_population(n, r_com, r_sens, T, T_ini, n_iterations, p_m, df):
	# linear interpolation to get t_f, t_m, and t_c
	df_c = df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].copy()
	values_n = list(sorted(df_c['n'].values))
	assert(len(values_n) == len(set(values_n)))
	df_c.set_index('n',inplace = True)
	df_c['t_ini'] = df_c['t_remove_targets_two'] + df_c['t_path_finder']

	if n < values_n[0]:
		print('no smaller instance already computed, \ntaking a portion of the minimum values') 
		min_n = values_n[0]
		t_f = (n/min_n) * df_c.at[min_n,'t_fusion']
		t_m = (n/min_n) * df_c.at[min_n,'t_mutation']
		t_c = (n/min_n) * df_c.at[min_n,'t_ini']
	elif n > values_n[-1]:
		print('no bigger instance already computed, \ntaking a portion of the maximum values') 
		max_n = values_n[-1]
		t_f = (n/max_n) * df_c.at[max_n,'t_fusion']
		t_m = (n/max_n) * df_c.at[max_n,'t_mutation']
		t_c = (n/max_n) * df_c.at[max_n,'t_ini']
	# linear interpolation
	else:
		k = 1
		while values_n[k] < n:
			k+=1
		n1 = values_n[k-1]
		n2 = values_n[k]
		r1 = (n2-n)/(n2-n1)
		r2 = (n-n1)/(n2-n1)
		t_f = r1 * df_c.at[n1,'t_fusion'] + r2 * df_c.at[n2,'t_fusion']
		t_m = r1 * df_c.at[n1,'t_mutation'] + r2 * df_c.at[n2,'t_mutation']
		t_c = r1 * df_c.at[n1,'t_ini'] + r2 * df_c.at[n2,'t_ini']

	s_pop_1 = int(T_ini/t_c)
	s_pop_2 = int(2*(T-T_ini)/(n_iterations*t_f + 2*p_m*t_m))
	if s_pop_1 < s_pop_2:
		print('limiting factor is the time needed for the initial population')
	else :
		print('limiting factor is the number of iterations')
	return min(s_pop_1,s_pop_2)


if __name__ == '__main__':
	p_mutation_min = 0.2
	p_mutation_max = 0.6
	n_iter = 100
	p_m = (11*p_mutation_min + 6.5*(p_mutation_max-p_mutation_min) + p_mutation_max*(n_iter - 10))/n_iter
	print(p_m)
	T = 60
	T_ini = 10

	df = clean_df('timings.csv')
	df.drop(df[df['n'] == 400].index, inplace = True)
	n_pop = size_population(400,r_com = 2, r_sens = 1,T = T,T_ini = T_ini, n_iterations = n_iter, p_m =  p_m, df = df)
	print('population of size : ',n_pop)
	data = Data(r_com = 2, r_sens = 1, file_name = 'Instances/captANOR400_10_80.dat')
	start = timer() 	
	b = optimize(data, n_pop, nb_iter_max = float('inf'), t_max = T, p_mutation_min = p_mutation_min, p_mutation_max = p_mutation_max, prop_children_kept = 0.8)
	print(b.compute_value())
	print('time needed :',timer() - start)
	# print(size_population(1510,1,1,T = 500, T_ini = 100, n_iterations = 5, p_m = 0.5, df = df))

	print('')
	n_iter = 100
	p_m = (11*p_mutation_min + 6.5*(p_mutation_max-p_mutation_min) + p_mutation_max*(n_iter - 10))/n_iter
	print(p_m)
	df = clean_df('timings.csv')
	df.drop(df[df['n'] == 625].index, inplace = True)
	n_pop = size_population(625,r_com = 3, r_sens = 2,T = T,T_ini = T_ini, n_iterations = n_iter, p_m =  p_m, df = df)
	print('population of size : ',n_pop)
	data = Data(r_com = 3, r_sens = 2, file_name = 'Instances/captANOR625_15_100.dat')
	start = timer() 	
	b = optimize(data, n_pop, nb_iter_max = float('inf'), t_max = T, p_mutation_min = p_mutation_min, p_mutation_max = p_mutation_max, prop_children_kept = 0.8)
	print(b.compute_value())
	print('time needed :',timer() - start)

	print('')
	n_iter = 100
	p_m = (11*p_mutation_min + 6.5*(p_mutation_max-p_mutation_min) + p_mutation_max*(n_iter - 10))/n_iter
	print(p_m)
	df = clean_df('timings.csv')
	df.drop(df[df['n'] == 900].index, inplace = True)
	n_pop = size_population(900,r_com = 2, r_sens = 2,T = T,T_ini = T_ini, n_iterations = n_iter, p_m =  p_m, df = df)
	print('population of size : ',n_pop)
	data = Data(r_com = 2, r_sens = 2, file_name = 'Instances/captANOR900_15_20.dat')
	start = timer() 	
	b = optimize(data, n_pop, nb_iter_max = float('inf'), t_max = T, p_mutation_min = p_mutation_min, p_mutation_max = p_mutation_max, prop_children_kept = 0.8)
	print(b.compute_value())
	print('time needed :',timer() - start)
