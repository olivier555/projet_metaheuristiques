import pandas as pd
import numpy as np
from data import Data
from optimize import optimize

"""
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
    stagnancy_max = 10

    bound = row['bound']
    try:
        solution, time, nb_iter = optimize(data, nb_population, nb_iter_max, t_max, p_mutation_min, p_mutation_max, prop_children_kept, stagnancy_max = stagnancy_max)
        dic_solution[(row['instance'],row['R_com'],row['R_capt'])] = [time, solution.compute_value(), solution.sensors, nb_iter, nb_population]
    except:
        fails.append(row)


print(fails)

df2 = pd.DataFrame.from_dict(dic_solution, orient = 'index')
df2.columns =  ['temps','valeur','capteurs','n_iterations','taille_pop']
df2.index.name = ['name','R_com','R_capt']
print(df2)
name_output = 'solutions_real_data.csv'
df2.to_csv(name_output)
"""

dico = {}
failed_grids = []
grid_widths = [10, 15, 20, 25, 30, 40]
for l in grid_widths:
    for (R_capt, R_com) in [(1,1),(1,2),(2,2),(2,3)]:
        data = Data(r_com = R_com, r_sens = R_capt, nb_rows = l, nb_columns = l)
        nb_population = 30
        nb_iter_max = 500
        t_max = 900 # 15 minutes
        p_mutation_min = 0.3
        p_mutation_max = 0.6
        prop_children_kept = 0.8
        stagnancy_max = 10
        try:
            solution, time, nb_iter = optimize(data, nb_population, nb_iter_max, t_max, p_mutation_min, p_mutation_max, prop_children_kept, stagnancy_max = stagnancy_max)
            dico[(l,R_capt,R_com)] = [time, solution.compute_value(), solution.sensors, nb_iter, nb_population]
        except :
            failed_grids.append((l,R_capt,R_com))

print(failed_grids)
df3 = pd.DataFrame.from_dict(dico, orient = 'index')
df3.columns =  ['temps','valeur','capteurs','n_iterations','taille_pop']
df3.index.name = ['grid_width','R_com','R_capt']
print(df3)
name_output = 'solutions_grids.csv'
df3.to_csv(name_output)
