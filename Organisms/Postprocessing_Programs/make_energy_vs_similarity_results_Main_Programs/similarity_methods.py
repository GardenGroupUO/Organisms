


def get_rCuts():
	first_nn = 1.0; second_nn = round(first_nn*(2.0**0.5),4)
	diff = second_nn - first_nn
	rCut_low = first_nn + (1.0/3.0)*diff
	rCut_high = first_nn + (2.0/3.0)*diff
	rCuts = np.linspace(rCut_low,rCut_high,78,endpoint=True)
	for index in range(len(rCuts)):
		rCuts[index] = round(rCuts[index],4)
	return rCuts

#def get_similarity_value_for_max_and_half(cluster_1_CNA_profile,cluster_2_CNA_profile):
def get_similarity_value_for_half(cluster_1_CNA_profile,cluster_2_CNA_profile):
	get_similarity_values = get_CNA_similarities(cluster_1_CNA_profile,cluster_2_CNA_profile)
	#return max(get_similarity_values), get_similarity_values[int(len(get_similarity_values)/2)]
	return get_similarity_values[int(len(get_similarity_values)/2)]