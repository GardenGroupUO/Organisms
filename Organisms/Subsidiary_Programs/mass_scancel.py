#!/usr/bin/python
'''
Geoffrey Weal, mass_scancel.py, 10/02/2021

This program is designed to cancel all the jobs between id_low and id_high in slurm.
'''
import os, sys
from subprocess import call, Popen

id_low = int(sys.argv[1])
id_high = int(sys.argv[2])

for scancel_id in range(id_low,id_high+1):
	args = ["scancel",str(scancel_id)]
	print('Cancelling Job id: '+str(scancel_id))
	p=Popen(args)