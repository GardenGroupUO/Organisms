import importlib
from packaging import version
#from distutils.version import StrictVersion

# Check the version of asap3 you are using
def check_version_of_asap3():

	asap3_spec = importlib.util.find_spec("asap3")
	found = asap3_spec is not None
	if not found:
		toString = ''
		toString += '\n'
		toString += '================================================\n'
		toString += 'This is the Organisms Program: A Genetic Algorithm for Nanoclusters\n'
		toString += 'Version: '+str(__version__)+'\n'
		toString += '\n'
		toString += 'The Organisms program requires asap3.\n'
		toString += '\n'
		toString += 'You are wanting to use one or more of the following:\n'
		toString += '   * SCM-based predation operator\n'
		toString += '   * structure + energy fitness operator\n'
		toString += 'These operators require asap3 to run, specifically asap3==3.11.10\n'
		toString += '\n'
		toString += "asap3 version 3.11.10 is specifically required because we have noticed a (core dump) issue that seems to occur during the genetic algorithm. Unfortunately, this error appears at seemingly random times so we don't know what the problem is, but it seems to be resolved if you use this version of asap3\n"
		toString += '\n'
		toString += 'Update your version of asap3 in pip by following the instruction in https://organisms.readthedocs.io/en/latest/Installation.html\n'
		toString += 'These instructions will ask you to install asap3 by typing the following into your terminal\n'
		toString += 'pip3 install --user --upgrade asap3=3.11.10\n'
		toString += '\n'
		toString += 'Install asap3 through pip by following the instruction in https://organisms.readthedocs.io/en/latest/Installation.html\n'
		toString += 'This program will exit before beginning\n'
		toString += '================================================\n'
		raise ImportError(toString)	

	import asap3
	asap3_required_version = '3.11.10'
	#if StrictVersion(asap3.__version__) < StrictVersion(asap3_version_minimum):
	if version.parse(asap3.__version__) < version.parse(ase_version_minimum):
		toString = ''
		toString += '\n'
		toString += '================================================\n'
		toString += 'This is the Organisms Program: A Genetic Algorithm for Nanoclusters\n'
		toString += 'Version: '+str(__version__)+'\n'
		toString += '\n'
		toString += 'The Organisms program requires asap3 greater equal to '+str(asap3_required_version)+'.\n'
		toString += 'The current version of asap3 you are using is '+str(asap3.__version__)+'.\n'
		toString += '\n'
		toString += 'You are wanting to use one or more of the following:\n'
		toString += '   * SCM-based predation operator\n'
		toString += '   * structure + energy fitness operator\n'
		toString += 'These operators require asap3 to run, specifically asap3==3.11.10\n'
		toString += '\n'
		toString += "asap3 version 3.11.10 is specifically required because we have noticed a (core dump) issue that seems to occur during the genetic algorithm. Unfortunately, this error appears at seemingly random times so we don't know what the problem is, but it seems to be resolved if you use this version of asap3\n"
		toString += '\n'
		toString += 'Update your version of asap3 in pip by following the instruction in https://organisms.readthedocs.io/en/latest/Installation.html\n'
		toString += 'These instructions will ask you to install asap3 by typing the following into your terminal\n'
		toString += 'pip3 install --user --upgrade asap3=3.11.10\n'
		toString += '\n'
		toString += 'This program will exit before beginning\n'
		toString += '================================================\n'
		raise ImportError(toString)