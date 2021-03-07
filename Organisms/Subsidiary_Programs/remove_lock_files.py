#!/usr/bin/python
'''
Geoffrey Weal, remove_lock_files.py, 10/02/2021

This program is designed to remove all the ga_running.lock files from subdirectories that this program is run from.
'''
import os, sys

lock_name = 'ga_running.lock'

path = os.getcwd()
for dirpath, dirs, files in os.walk(path):
	dirs.sort()
	if ('MDRun.py' in files and dirpath.split('/')[-1].startswith('Trial')) or ('run_eon.py' in files):
		if lock_name in files:
			print('Removing '+lock_name+' file in '+str(dirpath))
			os.remove(dirpath+'/'+lock_name)
		dirs[:] = []
		files[:] = []
	if ('Run.py' in files and dirpath.split('/')[-1].startswith('Trial')):
		if lock_name in files:
			print('Removing '+lock_name+' file in '+str(dirpath))
			os.remove(dirpath+'/'+lock_name)
		dirs[:] = []
		files[:] = []