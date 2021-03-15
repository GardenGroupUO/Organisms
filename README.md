# The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) Program: A Genetic Algorithm for Nanoclusters

[![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://dx.doi.org/10.1021/acs.jcim.0c01128)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Organisms)](https://docs.python.org/3/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/Organisms)](https://github.com/GardenGroupUO/Organisms)
[![PyPI](https://img.shields.io/pypi/v/Organisms)](https://pypi.org/project/Organisms/)
[![Conda](https://img.shields.io/conda/v/gardengroupuo/organisms)](https://anaconda.org/GardenGroupUO/organisms)
[![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://organisms.readthedocs.io/en/latest/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab)
[![Licence](https://img.shields.io/github/license/GardenGroupUO/Organisms)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/Organisms)](https://lgtm.com/projects/g/GardenGroupUO/Organisms/context:python)

Authors: Geoffrey R. Weal and Dr. Anna L. Garden (University of Otago, Dunedin, New Zealand)

Group page: https://blogs.otago.ac.nz/annagarden/

Page to cite with work from: *Development of a Structural Comparison Method to Promote Exploration of the Potential Energy Surface in the Global Optimisation of Nanoclusters*; Geoffrey R. Weal, Samantha M. McIntyre, and Anna L. Garden; JCIM; in submission stage.

## What is Organisms

The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) program is designed to perform a genetic algorithm global optimisation for nanoclusters. It has been designed with inspiration from the Birmingham Cluster Genetic Algorithm and the Birmingham Parallel Genetic Algorithm from the Roy Johnston Group (see ``J. B. A. Davis, A. Shayeghi, S. L. Horswell, R. L. Johnston, Nanoscale, 2015,7, 14032`` ([https://doi.org/10.1039/C5NR03774C](https://doi.org/10.1039/C5NR03774C) or [link to pdf here](https://pubs.rsc.org/en/content/articlepdf/2015/nr/c5nr03774c)), ``R. L. Johnston,Dalton Trans., 2003, 4193–4207`` ([https://doi.org/10.1039/B305686D](https://doi.org/10.1039/B305686D) or [link to pdf here](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.124.6813&rep=rep1&type=pdf)

## Try Organisms before you Clone/Pip/Conda (on Binder/Jupter Notebooks)!

If you are new to the Organisms program, it is recommended try it out by running Organisms live on our interactive Jupyter+Binder page before you download it. On Jupyter+Binder, you can play around with the Organisms program on the web. You do not need to install anything to try Organisms out on Jupyter+Binder. 

**Click the Binder button below to try Organisms out on the web! (The Binder page may load quickly or may take 1 or 2 minutes to load)**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab)

Have fun!

## What does Organisms have to offer to Nanocluster Global Optimisation

This program has been designed to learn about how to improve the efficiency of the genetic algorithm in locating the global minimum. This genetic algorithm implements various predation operators, fitness operators, and epoch methods. A structural comparison method based on the common neighbour analysis (CNA) has been implemented into a SCM-based predation operator and ''structure + energy'' fitness operator. 

The SCM-based predation operator compares the structures of clusters together and excludes clusters from the population that are too similar to each other. This can be tuned to exclude clusters that are structurally very similar to each other, to exclude clusters that are structurally different but of the same motif, or set to a custom structural exclusion setting. 

The ''structure + energy'' fitness operator is designed to include a portion of structural diversity into the fitness value as well as energy. The goal of this fitness operator is to guide the genetic algorithm around to unexplored areas of a cluster's potential energy surface. 

This genetic algorithm has been designed with Atomic Simulation Environment (ASE, [https://wiki.fysik.dtu.dk/ase/](https://wiki.fysik.dtu.dk/ase/)). with the use of ASE, clusters that are generated using the genetic algorithm are placed into databases that you can assess through the terminal or via a website. See more about how to the ASE database works [in the link here](https://wiki.fysik.dtu.dk/ase/ase/db/db.html?highlight=databases#id9).

The CNA has been implemented using ASAP3 (As Soon As Possible). See https://wiki.fysik.dtu.dk/asap for more information about ASAP3. 

## Installation

It is recommended to read the installation page before using the Organisms program. 

[organisms.readthedocs.io/en/latest/Installation.html](https://organisms.readthedocs.io/en/latest/Installation.html)

Note that you can install Organisms through ``pip3`` and ``conda``. 

## Where can I find the documentation for Organisms

All the information about this program is found online at [organisms.readthedocs.io/en/latest/](https://organisms.readthedocs.io/en/latest/). Click the button below to also see the documentation: 

[![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://organisms.readthedocs.io/en/latest/)

## About

<div align="center">

| Python | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Organisms)](https://docs.python.org/3/) | 
|:----------------------:|:-------------------------------------------------------------:|
| Repositories | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/Organisms)](https://github.com/GardenGroupUO/Organisms) [![PyPI](https://img.shields.io/pypi/v/Organisms)](https://pypi.org/project/Organisms/) [![Conda](https://img.shields.io/conda/v/gardengroupuo/organisms)](https://anaconda.org/GardenGroupUO/organisms) |
| Documentation | [![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://organisms.readthedocs.io/en/latest/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab) | 
| Citation | [![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://dx.doi.org/10.1021/acs.jcim.0c01128) | 
| Tests | [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/Organisms)](https://lgtm.com/projects/g/GardenGroupUO/Organisms/context:python)
| License | [![Licence](https://img.shields.io/github/license/GardenGroupUO/Organisms)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors | Geoffrey R. Weal, Dr. Anna L. Garden |
| Group Website | https://blogs.otago.ac.nz/annagarden/ |

</div>




