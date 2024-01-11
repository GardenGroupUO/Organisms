#!/usr/bin/env python3
'''
Did_Find_LES.py, Geoffrey Weal, 08/03/2019

This program will determine which of your genetic algorithm trials have completed up to a certain generation. 
'''
import os, sys, tarfile, shutil

if len(sys.argv) == 2:
    remove_trials_data = bool(sys.argv[1])
else:
    remove_trials_data = True

pycache_name = '__pycache__'
def tardir(dirpath, tar_name):
    with tarfile.open(tar_name, "w") as tar_handle:
        for root, dirs, files in os.walk(dirpath):
            dirs.sort()
            if pycache_name in dirs:
                dirs.remove(pycache_name)
            up_one_path = os.path.abspath(os.path.join(os.path.dirname(dirpath)))
            path_in_archive = os.path.relpath(root, up_one_path)
            print('tarring: '+str(path_in_archive))
            for file in files:
                tar_handle.add(os.path.join(root, file),arcname=os.path.join(path_in_archive, file))

def tar_all_files(dirpath):
    print('TARRING: '+str(dirpath))
    folder_name = dirpath # os.path.basename(os.path.normpath(path))
    tar_name = folder_name+'.tar'
    tardir(dirpath, tar_name)
    print('TARRED: '+str(dirpath))

def delete_folder(dirpath):
    print('DELETING: '+str(dirpath))
    shutil.rmtree(dirpath)
    print('DELETED: '+str(dirpath))

for dirpath, dirnames, filenames in os.walk(os.getcwd()):
    dirnames.sort()
    if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
        print('------------------------------------------------------------------------------')
        tar_all_files(dirpath)
        if remove_trials_data:
            delete_folder(dirpath)
        print('------------------------------------------------------------------------------')
        dirnames[:] = []
        filenames[:] = []