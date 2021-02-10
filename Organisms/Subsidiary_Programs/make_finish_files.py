#!/usr/bin/python
'''
Geoffrey Weal, make_finish_files.py, 10/02/2021

This program is designed to place finish files in all subdirectories that also include a Run.py file
'''
import os, sys

def make_finish_file(path):
	print('Putting finish file in '+str(path))
	finish_file = open(path+"/"+"finish", "w")
	finish_file.write('')
	finish_file.close()

path = os.getcwd()

for dirpath, dirs, files in os.walk(path):
	dirs.sort()
	if 'Run.py' in files:
		if any([(dir_name.startswith('Trial') and dir_name.replace('Trial','').isdigit()) for dir_name in dirs]):
			continue
		make_finish_file(dirpath)
		dirs[:] = []
		files[:] = []

	if 'MDRun.py' in files:
		trials = [dirname for dirname in dirs if dirname.replace('Trial','').isdigit()]
		for trial in trials:
			make_finish_file(dirpath+'/'+trial)
		dirs[:] = []
		files[:] = []

	if 'run_eon.py' in files:
		make_finish_file(dirpath)
		dirs[:] = []
		files[:] = []