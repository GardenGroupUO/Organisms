import os

def get_version_number():
  path_to_written_version = '../Organisms/__init__.py'
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

def write_meta_YAML(version):
  name_of_file = 'meta.yaml'
  with open(name_of_file,'w') as metaYAML:
    metaYAML.write('{% set version = "'+str(version)+'" %}\n')
    metaYAML.write('\n')
    metaYAML.write('package:\n')
    metaYAML.write('  name: organisms\n')
    metaYAML.write('  version: {{ version }}\n')
    metaYAML.write('\n')
    metaYAML.write('source:\n')
    metaYAML.write('  git_rev: {{ version }}\n')
    metaYAML.write('  git_url: https://github.com/GardenGroupUO/Organisms.git\n')
    metaYAML.write('\n')
    metaYAML.write('build:\n')
    metaYAML.write('  number: 1\n')
    metaYAML.write('  skip: true  # [win and py27 or win32]\n')
    metaYAML.write('  script: {{ PYTHON }} -m pip install . --no-deps -vv\n')
    metaYAML.write('\n')
    metaYAML.write('requirements:\n')
    metaYAML.write('  build:\n')
    metaYAML.write('    - python\n')
    metaYAML.write('    - setuptools\n')
    metaYAML.write('    - pip\n')
    metaYAML.write('  run:\n')
    metaYAML.write('    - python\n')
    metaYAML.write('    - numpy\n')
    metaYAML.write('    - scipy\n')
    metaYAML.write('    - ase\n')
    metaYAML.write('    - asap3\n')
    metaYAML.write('\n')
    metaYAML.write('about:\n')
    metaYAML.write('  home: https://github.com/GardenGroupUO/Organisms\n')
    metaYAML.write('  license: AGPL-3.0\n')
    metaYAML.write('  summary: "The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) program is a genetic algorithm designed to globally optimise nanoclusters (also known as clusters or nanoparticles)"\n')
    metaYAML.write('\n')
    metaYAML.write('# Build using: conda build .\n')

print('Writing meta.yaml to conda directory')
version = get_version_number()
write_meta_YAML(version)
print('Successfully finished writing meta.yaml to conda directory')