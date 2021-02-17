import os
from setuptools import setup
#from Organisms import __version__
#def get_version_number():
#  version = __version__
#  return version

def get_version_number():
  path_to_written_version = 'Organisms/__init__.py'
  with open(path_to_written_version) as initPY:
    for line in initPY:
      if line.startswith('__version__'):
        version = eval(line.rstrip().replace('__version__ = ',''))
        break
  return version

def get_long_description():
  this_directory = os.path.abspath(os.path.dirname(__file__))
  readme_file = os.path.join(this_directory, 'README.md')
  with open(readme_file, encoding='utf-8') as f:
    long_description = f.read()
  return long_description

def find_packages(root):
  packages = []
  for root, dirs, files in os.walk(root, topdown=False):
    for name in files:
      if name.endswith('.py'):
        file = os.path.relpath(os.path.join(root, name))
        dirname = os.path.dirname(file)
        rel_dirname = os.path.relpath(dirname)
        if not rel_dirname in packages:
          packages.append(rel_dirname)
  return sorted(packages)

def find_scripts():
  scripts = []
  scripts_folders = ['Subsidiary_Programs','Postprocessing_Programs','Helpful_Programs']
  for scripts_folder in scripts_folders:
    for root, dirs, files in os.walk('Organisms/'+scripts_folder, topdown=False):
      for file in files:
        if file.endswith('.py') and not 'Main' in file:
          filepath = os.path.relpath(os.path.join(root, file))
          scripts.append(filepath)
  return sorted(scripts)

setup(name='Organisms',
      packages=find_packages(root='Organisms'),
      scripts=find_scripts(),
      version=get_version_number(),
      description="This program is designed to perform a genetic algorithm global optimisation for nanoclusters.",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      author='Geoffrey R. Weal and Dr. Anna L. Garden',
      author_email='anna.garden@otago.ac.nz',
      url = 'https://blogs.otago.ac.nz/annagarden/',
      download_url = 'https://github.com/GardenGroupUO/Organisms/archive/v'+str(get_version_number())+'.tar.gz',
      license='GNU AFFERO GENERAL PUBLIC LICENSE',
      zip_safe=False,
      keywords = ['nanoclusters', 'nanoparticles', 'clusters', 'optimisation', 'genetic_algorithm'],
      install_requires=[
          'numpy','scipy','ase>=3.21.1','asap3>=3.11.10',
          'Sphinx','sphinx-rtd-theme','sphinx-tabs','sphinxcontrib-applehelp','sphinxcontrib-devhelp',
          'sphinxcontrib-htmlhelp','sphinxcontrib-jsmath','sphinxcontrib-plantuml','sphinxcontrib-qthelp',
          'sphinxcontrib-serializinghtml','sphinxcontrib-wiki'
          ],
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Science/Research',      # Define that your audience are developers
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Affero General Public License v3',   # Again, pick a license
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        ],
      )
