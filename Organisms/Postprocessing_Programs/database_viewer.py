#!/usr/bin/env python3
'''
Geoffrey Weal, database_viewer.py, 15/03/2021

There is a bug that occurs when you open the ASE database website. The metadata does not show.

This program allows the metadata to be included in the database for easier viewing of the website

'''
import sys
from subprocess import Popen #call, 

database_system_name = sys.argv[1]
#database_system_name = 'GA_Recording_Database.db'
path_to_metafile = 'Organisms/Helpful_Programs/meta.py'

args = ['ase','db',str(database_system_name),'-w','-M','Organisms']

p=Popen(args)
p.run()