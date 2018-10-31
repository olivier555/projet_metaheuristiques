import pandas as pd 
import matplotlib.pyplot as plt
import re
import numpy as np

df = pd.read_csv('timings.csv')


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

df['n,r_com,r_sens'] = df['n,r_com,r_sens'].apply(lambda x: list_from_str(x))
df['n'] = df['n,r_com,r_sens'].apply(lambda x: x[0])
df['r_com'] = df['n,r_com,r_sens'].apply(lambda x: x[1])
df['r_sens'] = df['n,r_com,r_sens'].apply(lambda x: x[2])
df.drop('n,r_com,r_sens', axis = 1, inplace = True)
# df.set_index(['n','r_com','r_sens'], inplace = True)


# for n in df.columns:
# 	df[n] = df[n].apply(lambda x: list_from_str(x)[0])


# 
list_r = [(1,1), (2,1),(2,2),(3,2)]
df['tps_ini'] = df['t_remove_targets_two'] + df['t_path_finder']


plt.close('all')
plt.figure(1)
ax = plt.subplot(111)
for (r_com,r_sens) in list_r:
	df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].sort_values(by = 'n').plot(x = 'n',y = 'tps_ini', ax = ax)
# plt.show()# plt.show()


ax.legend(['t_ini for (r_com, r_sens) = ' + str(i) for i in list_r])

plt.figure(2)
ax = plt.subplot(111)
for (r_com,r_sens) in list_r:
	df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].sort_values(by = 'n').plot(x = 'n',y = 't_mutation', ax = ax)
	df[np.logical_and(df['r_com'] == r_com, df['r_sens'] == r_sens)].sort_values(by = 'n').plot(x = 'n',y = 't_fusion', ax = ax)

l = []
for i in list_r:
	l = l + ['t_mutation for (r_com, r_sens) = ' + str(i), 't_fusion for (r_com, r_sens) = ' + str(i)]
print(l)
ax.legend(l)
plt.show()# plt.show()
