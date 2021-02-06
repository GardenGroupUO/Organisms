#!/usr/bin/python

import os, sys
from subprocess import call, Popen

id_low = int(sys.argv[1])
id_high = int(sys.argv[2])

for scancel_id in range(id_low,id_high+1):
	args = ["scancel",str(scancel_id)]
	print('Cancelling Job id: '+str(scancel_id))
	p=Popen(args)