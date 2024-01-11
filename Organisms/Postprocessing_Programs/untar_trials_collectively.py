#!/usr/bin/env python3
'''
Did_Find_LES.py, Geoffrey Weal, 08/03/2019

This program will determine which of your genetic algorithm trials have completed up to a certain generation. 
'''
import os, sys, tarfile

if len(sys.argv) == 2:
    remove_trials_data = bool(sys.argv[1])
else:
    remove_trials_data = True

pycache_name = '__pycache__'
def untar(dirpath, tar_name):
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

def untar_a_tar_file(dirpath,filename):
    path_to_tar = dirpath+'/'+filename
    print('UNTARRING: '+str(path_to_tar))
    with tarfile.open(path_to_tar) as tar_handle:
        tar_handle.extractall(dirpath)
    print('UNTARRED: '+str(path_to_tar))

def delete_tar(path_to_tar):
    print('DELETING: '+str(path_to_tar))
    os.remove(path_to_tar)
    print('DELETED: '+str(path_to_tar))

for dirpath, dirnames, filenames in os.walk(os.getcwd()):
    dirnames.sort()
    if any([filename.endswith('.tar') for filename in filenames]):
        dirnames[:] = []
        for filename in filenames:
            print('------------------------------------------------------------------------------')
            untar_a_tar_file(dirpath,filename)
            if remove_trials_data:
                path_to_tar = dirpath+'/'+filename
                delete_tar(path_to_tar)
            print('------------------------------------------------------------------------------')
        filenames[:] = []