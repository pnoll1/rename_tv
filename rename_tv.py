#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 18:18:53 2017

@author: pat
Require python 3.6 for os functions
"""
import os
import shutil
from pathlib import Path
from sys import argv
import requests

directory_video = Path('/home/pat/Videos/')


def generate(episodes):
    '''input: comma seperarted list of episodes on each disc
    output: dictionary with keys that are disc numbers and
    values of matching strings for episodes on each disc'''
    targets = {}
    n = 1
    m = 0
    l = 1
    k = int(episodes[m]) + 1
    replace_string = 'E'
    while n <= len(episodes):
        ep_list = list(range(l, k))
        for j in ep_list:
            if j != ep_list[len(ep_list)-1]:
                replace_string = replace_string + str(j) + '_'
            else:
                replace_string = replace_string + str(j)
        targets["D" + str(n)] = replace_string
        if n == len(episodes):
            break
        replace_string = 'E'
        l = k
        m += 1
        k = int(episodes[m]) + l
        n += 1
    return targets


def s_a_d(directory, targets):
    '''finds keys of targets and replaces keys with values in selected text'''
    paths_original = []
    paths_new = []
    for filename in directory.iterdir():
        for j in targets.keys():
            if j in filename.name:
                path_original = filename
                path_new = Path(filename.name.replace(j, targets.get(j)))
                # path_new = os.path.join(filename_zero.replace(j, targets.get(j) + extension))
                os.rename(path_original,path_new)
                paths_original.append(path_original)
                paths_new.append(path_new)
    return paths_original,paths_new

# translates command line arguments into format for generate
episode_string = argv[1]
episode_list = episode_string.split(',') # list containing strings
# runs generate to create dictionary for what to find and replace
episode_list_formatted = generate(episode_list)
# remove map files
os.chdir(directory_video)
os.system('rm *.map')
# renames files to Kodi format and keeps paths for processing
paths_discs_original, paths_discs_new = s_a_d(directory_video, episode_list_formatted)
# operations to get show name
disc_number = list(episode_list_formatted.keys())
path_show = paths_discs_original[0].stem
season = path_show[-3]
for d in disc_number:
    disc_identifier = '_S'+str(season)+d
    path_show = path_show.replace(disc_identifier,'')
# create folder on server if needed
tv_directory = '/home/pat/NAS/TV/'
try:
    os.mkdir(tv_directory+path_show)
except  FileExistsError:
    pass
# move files
for path in paths_discs_new:
    shutil.move(path,tv_directory+path_show+'/'+path.name)

# Tell Kodi to scan for new video files
try:
    req = requests.get('http://desktop:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.Scan","id":1}')
except  requests.exceptions.RequestException as e:
    print("Couldn't reach Desktop Kodi")
try:
    req2 = requests.get('http://192.168.1.6:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.Scan","id":1}')
except  requests.exceptions.RequestException as e:
    print("Couldn't reach RPi")
# check database and remove files from wanted list
