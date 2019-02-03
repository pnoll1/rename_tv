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
import re

directory_video = Path('/home/pat/Videos/')
tv_directory = Path('/home/pat/NAS/TV/')

def generate(episodes):
    '''input: comma seperarted list of episodes on each disc
    output: dictionary with keys that are disc numbers and
    values of matching strings for episodes on each disc
    org_type = 1 is multiple epsisode per file
    org_type = 0 is 1 episode per file in folders by disc'''
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

def s_g_d(directory, episodes):
    '''grabs folder name, seperates out relevant info, generates new filenames,
    replaces old filenames with new'''
    # grab folder name
    for filename in sorted(directory.iterdir()):
        path_show = filename
        break
    # grab show name from folder name
    # grab season from folder name
    path_show = path_show.stem
    season_number = path_show[-3]
    show_list = []
    disc_identifier = '_S'+str(season_number)+'D1'
    show_name = path_show.replace(disc_identifier,'')
    # construct replacement strings        
    for i in range(1, (episodes+1)):
        episode = 'E' + str(i)
        path_show = Path(show_name +'_S' + season_number + episode + '.mkv')
        show_list.append(path_show)
    # create folder on server if needed
    try:
        os.mkdir(tv_directory.joinpath(show_name))
    except FileExistsError:
        pass
    j = 0
    paths =[]
    # loop through each disc folder, low to high
    for directory_name in sorted(directory.iterdir()):
        os.chdir(directory_name)
        # loop through each file in folder, low to high
        for filename in sorted(Path.cwd().iterdir()):
            # rename each file, then move
            os.rename(filename, show_list[j])
            print('Transferring file {}'.format(str(j+1)))
            shutil.move(show_list[j],tv_directory.joinpath(show_name,show_list[j]))
            print('Finished Transferring file {}'.format(str(j+1)))
            paths.append(show_list[j])
            if j == episodes:
                break
            j += 1
    return paths, path_show
# translates command line arguments into format for generate
org_type = argv[2]
episode_string = argv[1]
episode_list = episode_string.split(',') # list containing strings
# runs generate to create dictionary for what to find and replace
if org_type == 1:
    episode_list_formatted = generate(episode_list, org_type)
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
    try:
        os.mkdir(tv_directory+path_show)
    except  FileExistsError:
        pass
    # move files
    for path in paths_discs_new:
        shutil.move(path,tv_directory+path_show+'/'+path.name)
else:
    episodes = 0
    for i in episode_list:
        episodes += int(i)
    paths, path_show = s_g_d(directory_video, episodes)

# Tell Kodi to scan for new video files
try:
    req = requests.get('http://desktop:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.Scan","id":1}')
except  requests.exceptions.RequestException as e:
    print("Couldn't reach Desktop Kodi")
try:
    req2 = requests.get('http://192.168.1.11:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.Scan","id":1}')
except  requests.exceptions.RequestException as e:
    print("Couldn't reach RPi")
# check database and remove files from wanted list
