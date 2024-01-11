#!/usr/bin/env python3

from os      import walk, remove, listdir, getcwd
from os.path import isfile, getsize

def is_file_empty(file_name):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return isfile(file_name) and getsize(file_name) == 0

def remove_black_arrayjobs(dirpath):
    print('Looking in: '+dirpath)
    arrayJobs = [file for file in listdir(dirpath) if (isfile(dirpath+'/'+file) and file.startswith('arrayJob_'))]
    arrayJobs.sort()
    for arrayJob in arrayJobs:
        path_to_arrayJob = dirpath+'/'+arrayJob
        if is_file_empty(path_to_arrayJob):
            print('Removing: '+str(path_to_arrayJob))
            remove(path_to_arrayJob)

print('=============================================================')
print('Removing arrayJob files that are found in a mass_submit folder and are blank.')
print()
print('If arrayJob files are blank, this means the arrayjob packet finished.')
print('-------------------------------------------------------------')
for dirpath, dirnames, filenames in walk(getcwd()):
    print(dirpath)
    dirnames.sort()
    if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
        remove_black_arrayjobs(dirpath)
        dirnames[:] = []
        filenames[:] = []
print('=============================================================')
