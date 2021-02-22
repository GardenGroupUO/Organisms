



def minmise(cluster):
	cluster.set_cell((1000,1000,1000))
	cluster.center()
	cluster = Minimisation_Function(cluster)
	#cluster.set_cell((10,10,10))
	#cluster.center()
	return cluster



