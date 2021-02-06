#!/usr/bin/python

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