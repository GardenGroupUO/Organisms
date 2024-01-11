#!/usr/bin/env python3

from os      import walk, remove, listdir, getcwd
from os.path import isfile, getsize

def is_file_empty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return isfile(file_path) and getsize(file_path) == 0

def remove_black_arrayjobs(dirpath):
    print('Removing arrayJobs from: '+str(dirpath))
    arrayJobs = [file for file in listdir(dirpath) if (isfile(dirpath+'/'+file) and file.startswith('arrayJob_'))]
    arrayJobs.sort()
    for arrayJob in arrayJobs:
        path_to_arrayJob = dirpath+'/'+arrayJob
        remove(path_to_arrayJob)



print('=============================================================')
print('Removing arrayJob files that are found in a mass_submit folder that have not been transferred to their Trial folder.')
print('-------------------------------------------------------------')
for dirpath, dirnames, filenames in walk(getcwd()):
    print(dirpath)
    dirnames.sort()
    if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
        remove_black_arrayjobs(dirpath)
        dirnames[:] = []
        filenames[:] = []
print('=============================================================')
