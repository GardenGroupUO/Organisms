import numpy as np

def get_distance(atom1,atom2):
    """
    This gives the distance between two atoms in a cluster. 

    :returns: The distance between two atoms in a cluster
    :rtype:   float

    """
    x_dist = atom1.x - atom2.x
    y_dist = atom1.y - atom2.y
    z_dist = atom1.z - atom2.z
    distance = (x_dist**2.0 + y_dist**2.0 + z_dist**2.0)**0.5
    return distance

def get_cluster_distance_list(cluster, neighbor_cutoff):
    """
    This method give a list of the interatomic distances between evety atom in the cluster. 

    :param cluster: This is the cluster to get all the interatomic distances between every atom. 
    :type  cluster: Organisms.GA.Cluster.Cluster
    :param neighbor_cutoff: If desired, this method can be programmed to not include any distances that are larger than some cutoff value. Given in Angstroms.
    :type  neighbor_cutoff: float

    :returns: A list of all the interatomic distances between every atom in the cluster. 
    :rtype:   float

    """
    list_of_distances = []
    for index_a1 in range(len(cluster)):
        for index_a2 in range(index_a1+1,len(cluster)):
            distance = get_distance(cluster[index_a1],cluster[index_a2])
            list_of_distances.append(distance)
    list_of_distances.sort()
    list_of_distances = np.array(list_of_distances)
    return list_of_distances

########################################################################################

def LoD_compare_two_structures(LoD_1, LoD_2, percentage_diff):
    """
    This method will determine if these two clusters are structurally similar or not based on the IDCM

    :param LoD_1: This is the list of the interatomic distances in cluster 1
    :type  LoD_1: list of floats
    :param LoD_2: This is the list of the interatomic distances in cluster 2
    :type  LoD_2: list of floats
    :param percentage_diff: If the differences between all the distances in LoD_1 and LoD_2 are less than this percentage difference, they are the same. If any one difference is greater than this percentage, the two clusters are different. 
    :type  percentage_diff: float

    :returns: If the differences between all the distances in LoD_1 and LoD_2 are less than percentage_diff, they are the same. If any one differences in creater than percentage_diff percent, the two clusters are different. 
    :rtype:   bool. 

    """
    similar_element_list = []
    for index in range(len(LoD_1)):
        distance1 = LoD_1[index]
        distance2 = LoD_2[index]
        distance_difference_percentage = (float(abs(distance1 - distance2))/float(min([distance1,distance2])))*100.0
        if abs(distance_difference_percentage) <= float(percentage_diff):
            pass
        else:
            return False
    return True

