'''
CNA_Entry.py, Geoffrey Weal, 29/10/2018

This class holds a CNA comparison entry between two clusters, Cluster cluster_1 and Cluster cluster_2, including
the similarity_profile for different values of rCut, the average and the result of the comparison, 
based on the result from Geoff's Thesis

'''
import sys

def get_comparison(percentage_similarities):
	'''
	From the information from self.percentage_similarities, this method will write the result of the 
	comparison into self.similarity_category, as determined from the proceedure created by Geoffrey Weal.

	:param percentage_similarities: These are a list of all the similarities from performing the SCM across many rCut values.
	:type  percentage_similarities: list of floats

	:returns: The similarity class that the pair of clusters is assigned to based on the percentage_similarities, and the maximum similarity of percentage_similarities
	:rtype:   a str. and a float

	'''
	maximum_similarity = max(percentage_similarities)
	if   maximum_similarity == 100.0:
		similarity_category = 'geometric'
	elif maximum_similarity >= 50.0:
		similarity_category = 'same motif'
	else:
		similarity_category = 'different'
	return similarity_category, maximum_similarity

class Similarity_Profile:
	'''
	This class holds a CNA comparison entry between two clusters, Cluster 1 and Cluster 2, including
	the similarity_profile for different values of rCut, the average and the result of the comparison, 
	based on the result from Geoff's Thesis

	:param name_1: Name of the first cluster.
	:type  name_1: int
	:param name_2: Name of the first cluster.
	:type  name_2: int
	:param similarity_profile: The similarity profile between cluster 1 and cluster 2.
	:type  similarity_profile: list of floats
	
	'''
	def __init__(self,name_1, name_2, similarity_profile):
		if name_1 < name_2:
			self.name_1 = name_1; self.name_2 = name_2; 
		elif name_1 > name_2:
			self.name_1 = name_2; self.name_2 = name_1; 
		else:
			exit('Error')
		self.similarity_profile = similarity_profile
		self.get_results()

	def __repr__(self):
		"""
		This is what the terminal will print to represent your class. 
		"""
		toString = str(self.name_1)+'Vs.'+str(self.name_2)
		return toString

	def get_results(self):
		'''
		Get the result of the average of similarity_profile, and the result of the comparison.
		'''
		self.get_comparison()
		self.get_average()

	def get_average(self):
		'''
		Get the average of similarity_profile
		'''
		self.average = float(sum(self.similarity_profile))/float(len(self.similarity_profile))

	def get_comparison(self):
		'''
		From the information from self.similarity_profile, this method will write the result of the 
		comparison into self.similarity_category, as determined from the proceedure created by Geoffrey Weal.
		'''
		self.similarity_category, self.similarity_max = get_comparison(self.similarity_profile)







