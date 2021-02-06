#!/usr/bin/python

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