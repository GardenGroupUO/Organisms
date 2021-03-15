# The information about the Organisms program

__name__    = 'The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) Program'
__version__ = '3.2.6'
__author__  = 'Geoffrey Weal and Dr. Anna Garden'

import sys
if sys.version_info[0] == 2:
	toString  = '================================================'+'\n'
	toString += 'This is the Organisms Program: A Genetic Algorithm for Nanoclusters'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Organisms program requires Python3. You are attempting to execute this program in Python2.'+'\n'
	toString += 'Make sure you are running the Organisms program in Python3 and try again'+'\n'
	toString += 'This program will exit before beginning'
	raise ImportError(toString)

__author_email__ = 'anna.garden@otago.ac.nz'
__license__ = 'GNU AFFERO GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/GardenGroupUO/Organisms'
__doc__ = 'See https://organisms.readthedocs.io/en/latest/ for the documentation on this program'

from Organisms.GA.GA_Program import GA_Program
from Organisms.Subsidiary_Programs.MakeTrialsProgram import MakeTrialsProgram
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results import make_energy_vs_similarity_results
#from Organisms.Subsidiary_Programs.GetNewlyInitilisedPopulation import GetNewlyInitilisedPopulation
__all__ = ['GA_Program','MakeTrialsProgram','make_energy_vs_similarity_results'] # 'GetNewlyInitilisedPopulation']
