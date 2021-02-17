import sys
if sys.version_info[0] == 2:
	raise ImportError('The Organisms program requires Python3. This is Python2.')

__name__    = 'The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) Program'
__version__ = '3.2.4'
__author__  = 'Geoffrey Weal and Dr. Anna Garden'

__author_email__ = 'anna.garden@otago.ac.nz'
__license__ = 'GNU AFFERO GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/GardenGroupUO/Organisms'
__doc__ = 'See https://organisms.readthedocs.io/en/latest/ for the documentation on this program'

from Organisms.GA.GA_Program import GA_Program
from Organisms.Subsidiary_Programs.MakeTrialsProgram import MakeTrialsProgram
#from Organisms.Subsidiary_Programs.GetNewlyInitilisedPopulation import GetNewlyInitilisedPopulation
__all__ = ['GA_Program','MakeTrialsProgram'] # 'GetNewlyInitilisedPopulation']
