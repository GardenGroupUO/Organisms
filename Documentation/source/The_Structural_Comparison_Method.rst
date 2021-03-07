
.. _The_Structural_Comparison_Method:

The Structural Comparison Method (SCM)
######################################

The structural comparison method (SCM) was created and designed to identify the structural similarity between various clusters. There are two versions of the implemetation of this algorithm. These are the Total Structural Comparison Method (T-SCM), and the Atom-by-Atom Structural Comparison Method (A-SCM). 

Both of these methods use the Common Neighbour Analysis (CNA) to provide a description of the structure of a cluster. The CNA is a tool designed to describe all the local structural environments about a cluster. It does this by assigning signatures that describe the number of neighbouring atoms between two neighbouring (or bonded) atoms. More information about the CNA can be found at `D Faken, H Jónsson, Comput. Mater. Sci., 1994, 2, 279-286 <https://notendur.hi.is/hj/papers/paperCNanal.pdf>`_, while examples of the CNA can be found at `N. Lümmen and T. Kraska, Model. Simul. Mater. Sci. Eng., 2007, 15, 3, <https://iopscience.iop.org/article/10.1088/0965-0393/15/3/010>`_.

An important note to take about the CNA is that the user is required to provide a value of rCut, which is the maximum distance between two atoms for those two atoms to be considered neighbours (or bonded). 

These provide a list of CNA signatures, and the amount of each CNA signature in total or on each atom. A secondary method compares these lists (of CNA signatures) to provide a value of the structural similarity between two clusters. Performing the SCM over a range of rCut values allows the SCM to assign a similarity class to the comparison of those two clusters. The three classes are:

	* **Class I**: Two structures are structurally identical or geometrically similar.
	* **Class II**: Two structures are structurally different, but have the same motif.
	* **Class III**: Two structures are structurally different, and are of different motifs.

For more information about the SCM, see XXX

The Total Structural Comparison Method (T-SCM)
**********************************************

This method will tally the number of each CNA signature across the whole cluster. 

The Atomic Structural Comparison Method (A-SCM)
***********************************************