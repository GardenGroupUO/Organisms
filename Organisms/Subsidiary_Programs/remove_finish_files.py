#!/usr/bin/python
'''
Geoffrey Weal, remove_finish_files.py, 10/02/2021

This program is designed to remove all the finish files from subdirectories that this program is run from.
'''
import os, sys

path = os.getcwd()
for dirpath, dirs, files in os.walk(path):
	dirs.sort()
	if ('MDRun.py' in files and dirpath.split('/')[-1].startswith('Trial')) or ('run_eon.py' in files):
		if 'finish' in files:
			print('Removing finish file in '+str(dirpath))
			os.remove(dirpath+'/finish')
		dirs[:] = []
		files[:] = []
	if ('Run.py' in files and dirpath.split('/')[-1].startswith('Trial')):
		if 'finish' in files:
			print('Removing finish file in '+str(dirpath))
			os.remove(dirpath+'/finish')
		dirs[:] = []
		files[:] = []