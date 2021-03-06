"""
Class graph used to code a graph
"""

import numpy as np

class Graph():
	# if edges_values != None we iniate the graph with values on the edges.
	# edges_values_dic and edges_values_matrix are boolean to kwon if we save the values
	# in a matrix or in a dictionnary

	# if adjacency is None we compute it from edges_values but we need to make sure tha edges_value is not None

	# triangular_sup is a boolean to say that the graph is not oriented and that the adjacency matrix can be computed by taking in argument only the upper
	# part of the given adjacency matrix

	#  edges_value_matrix and edges_value_dic are two booleans to say if we want to save the edges values in a matrix or in a dictionnary 
	def __init__(self,n,adjacency = None, oriented = False, triangular_sup = False, edges_value=None, edges_value_matrix = True, edges_value_dic = True):
		self.n = n
		# adajacency and edges_value can't be both None to initiate the graph
		assert (adjacency is not None) or (edges_value is not None)

		if triangular_sup :
			assert np.allclose(adjacency, np.triu(adjacency)), "matrix of adjacency is not upper triangular" 
			assert isinstance(adjacency, np.ndarray), "adjacency is not an array"
			adjacency = adjacency + adjacency.T
			assert not(oriented)
		self.oriented = oriented
		
		if edges_value is None:
			self.value = False # there are no values (or capacities) on the edges
			self.adjacency = (adjacency != 0)
		else:
			if triangular_sup and isinstance(edges_value, np.ndarray):
				edges_value = edges_value + edges_value.T 
			self.value = True
			self.edges_value_matrix = edges_value_matrix
			self.edges_value_dic = edges_value_dic
			# save the value of edges_value 
			self.save_edges_values(adjacency,edges_value)
		
		assert self.adjacency.shape == (n,n), "adjacency matrix size doesn't fit the number of vertex"
		assert oriented or np.allclose(self.adjacency, self.adjacency.T),"matrix of adjacency is not triangular but oriented = False"
		
		#dictionnary of neighbours for each vertex
		self.neighbours = {}
		for i in range(self.n):
			self.neighbours[i] = list(np.where(self.adjacency[i])[0])
		self.m = sum(sum(self.adjacency))/(1 + oriented)
		
	# this function save the value in edges_value.
	# edges_value argument can be an array or a dictionnary.
	# if self.edges_value_matrix is true we save this in a dictionnary
	# if self.edges_value_di is true we save those value in a dictionnary
	def save_edges_values(self, adjacency, edges_value):
		if isinstance(adjacency,np.ndarray):
			self.adjacency = adjacency
			assert adjacency.shape == (self.n,self.n), "adjacency matrix size doesn't fit the number of vertex"
			adjacency_already_built = True
		else:
			adjacency_already_built = False
		#booleans to know if we want to save the matrix or the dictionnary
		assert self.edges_value_matrix or self.edges_value_dic, "we need to save the value on the edges somewhere"
		
		if isinstance(edges_value,dict):
			if self.edges_value_dic :
				self.edges_value_d = edges_value
			if self.edges_value_matrix :
				self.edges_value_m = np.zeros((self.n,self.n))
				for (i,j), value in self.edges_value_d.items():
					self.edges_value_m[i][j] = value
			
			if not(adjacency_already_built):
				self.adjacency = np.zeros((self.n,self.n), dtype = 'bool')
				for (i,j), value in self.edges_value_d.items():
					self.adjacency[i][j] = True
			else:
				print("warning, adjacency matrix and dictionnary of edges values given separately")
		else:
			if not(adjacency_already_built):
				self.adjacency = np.ones((self.n,self.n),dtype = 'bool')
			assert isinstance(edges_value,np.ndarray), "type of edges_value not known"
			assert edges_value.shape == (self.n,self.n), "edges_value matrix shape doesn't fit n"
			assert isinstance(self.adjacency,np.ndarray) and self.adjacency.shape == (self.n,self.n), "adjacency is not a square matrix of size n"
			if self.edges_value_matrix :
				self.edges_value_m = edges_value
			else:
				self.edges_value_m = None
			if self.edges_value_dic :
				self.edges_value_d = {}
				for i in range(self.n):
					for j in range(i+1,self.n):
						if self.adjacency[i][j]:
							self.edges_value_d[(i,j)] = edges_value[i][j]
							self.edges_value_d[(j,i)] = edges_value[j][i]
			else:
				self.edges_value_d = None
		if self.edges_value_matrix:
			assert self.oriented or np.allclose(self.edges_value_m, self.edges_value_m.T, atol = 1e-8),"matrix edges_value is not symmetric but oriented = False"
		if not(self.oriented) and self.edges_value_dic:
			for (i,j) in self.edges_value_d.keys():
				assert j<=i or self.edges_value_d[(i,j)] == self.edges_value_d[(i,j)], "edges_value dictionnary is not symmetric"



	def get_neighbours(self,i):
		return self.neighbours[i]

	# test if the graph is bipartite
	def is_bipartite(self):
		left = set([0])
		right = set()
		reached = set()
		new = set([0])
		visit_left = True
		n = self.n
		while len(reached) < n:
			while len(new) > 0: 
				neighbours = set()
				for i in new:
					neighbours = neighbours.union(self.get_neighbours(i))
				if visit_left :
					if len(left.intersection(neighbours)) > 1:
						return (False,[])
					else:
						right = right.union(neighbours)
				else:
					if len(right.intersection(neighbours)) > 1:
						return (False,[])
					else:
						left = left.union(neighbours)

				reached = reached.union(new)
				new = neighbours - reached
				visit_left = not(visit_left)
			for i in range(n):
				if i not in reached:
					new = set([i])
					left = left.union(set([i]))
					reached = reached.union(set([i]))
					visit_left = True
					break
		return (True,[list(left),list(right)])

	def get_size(self):
		return self.n

	#kruskal algorithm to to compute the minimum spanning tree in a graph
	def kruskal(self):
		assert not(self.oriented)
		list_value_edges = []
		list_index_edges = []
		for i in range(self.n):
			for j in self.neighbours[i]:
				if i < j:
					list_value_edges.append(self.edges_value_d[(i,j)])
					list_index_edges.append((i,j))  
		
		sorted_index = np.argsort(list_value_edges)

		compt = 0
		ind = 0
		ind_edges = []
		connex_set = {}
		connex_set_index = {}
		for i in range(self.n):
			connex_set[i] = {i}
			connex_set_index[i] = i
		while compt < self.n-1:
			(j,k) = list_index_edges[sorted_index[ind]]
			ind_set_j = connex_set_index[j]
			ind_set_k = connex_set_index[k]
			if (j not in connex_set[ind_set_k]):
				ind_new_set = min(ind_set_j,ind_set_k)
				for l in connex_set[ind_set_j]:
					connex_set_index[l] = ind_new_set
				for l in connex_set[ind_set_k]:
					connex_set_index[l] = ind_new_set
				connex_set[ind_new_set] = connex_set[ind_set_j].union(connex_set[ind_set_k])
				connex_set_index[j] = ind_new_set
				connex_set_index[k] = ind_new_set
				compt += 1
				ind_edges.append(sorted_index[ind])
			ind += 1

		adj = np.zeros((self.n,self.n),dtype = 'bool')
		edges_value = np.zeros((self.n,self.n))
		for k in ind_edges :
			(i,j) = list_index_edges[k]

			adj[i][j] = True
			adj[j][i] = True
			v = list_value_edges[k]
			edges_value[i][j] = v
			edges_value[j][i] = v
		return (adj, edges_value)





# some tests of the graph class
if __name__ == '__main__':
	g = Graph(5,None,oriented = False, triangular_sup = False,edges_value = {(1,2):3,(2,1):3})
	print(g.get_neighbours(3))
	try :
		g = Graph(5,None,oriented = False,triangular_sup = False,edges_value = {(1,2):3,(2,1):1})
	except AssertionError as e: 
		print(e)

	g = Graph(5,np.zeros((5,5)), True)
	try :
		g = Graph(5,np.zeros((5,6)), True)
	except AssertionError as e:
		print(e)

	a = np.zeros((5,5))
	a[4][1] = 1
	a[1][4] = 1
	g = Graph(5,a, False)
	print("test biparti", g.is_bipartite())

	a[1][4] = 0
	
	try :
		g = Graph(5,a, False)
	except AssertionError as e:
		print(e)

