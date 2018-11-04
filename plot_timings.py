import pandas as pd 
import matplotlib.pyplot as plt
import re
import numpy as np

# this script need to be used after elementar_timings.csv
# it's a plot of the different function timings depending on the size of the instance

NAME_CSV = 'timings.csv'
df = pd.read_csv(NAME_CSV)


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

# changing the index of the dataframe to filter it on (r_com,r_sens) later
df['n,r_com,r_sens'] = df['n,r_com,r_sens'].apply(lambda x: list_from_str(x))
df['n'] = df['n,r_com,r_sens'].apply(lambda x: x[0])
df['r_com'] = df['n,r_com,r_sens'].apply(lambda x: x[1])
df['r_sens'] = df['n,r_com,r_sens'].apply(lambda x: x[2])
df.drop('n,r_com,r_sens', axis = 1, inplace = True)



list_r = [(1,1), (2,1),(2,2),(3,2)]
#initial timing for one slution as a combination of the different methods used 
df['tps_ini'] = df['t_remove_targets_two'] + df['t_path_finder'] + df['t_switch_ini'] + df['t_remove_targets_ini']

# Figures to plot
plt.close('all')
plt.figure(1)
ax = plt.subplot(111)
for (r_com,r_sens) in list_r:
	df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].sort_values(by = 'n').plot(x = 'n',y = 'tps_ini', ax = ax, style = '-o')
plt.ylabel('secondes')
plt.xlabel('nombre de points')
plt.title("Temps moyen de création d'une solution initiale \n en fonction du nombre de points")

ax.legend(['(r_com, r_capt) = ' + str(i) for i in list_r])

plt.figure(2)
ax = plt.subplot(111)
for (r_com,r_sens) in list_r:
	df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].sort_values(by = 'n').plot(x = 'n',y = 't_fusion', ax = ax, style = '-d')

ax.legend(['(r_com, r_capt) = ' + str(i) for i in list_r])
plt.title("Temps moyen d'une fusion \n en fonction du nombre de points")
plt.ylabel('secondes')
plt.xlabel('nombre de points')

plt.figure(3)
ax = plt.subplot(111)
for (r_com,r_sens) in list_r:
	df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].sort_values(by = 'n').plot(x = 'n',y = 't_mutation', ax = ax, style = '-o')

ax.legend(['(r_com, r_capt) = ' + str(i) for i in list_r])
plt.title("Temps moyen d'une mutation \n en fonction du nombre de points")
plt.ylabel('secondes')
plt.xlabel('nombre de points')
plt.show()