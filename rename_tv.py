#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 18:18:53 2017

@author: pat
Require python 3.6+ for os functions
"""
import os
import shutil
from pathlib import Path
import argparse
import requests
import re

parser = argparse.ArgumentParser(description='renumber tv episodes for proper indexing in kodi. file names or folders must follow show_S1D1 format')
parser.add_argument('--episodes-per-disc', nargs='+',type=int, help='episodes per disc')
parser.add_argument('--many-per-file', action='store_true', help='many videos in one file, common for isos')
parser.add_argument('--one-per-file', action='store_true', help='1 video per file, common for mkv')
parser.add_argument('--start', nargs='?', default=1, type=int, help='episode number to start numbering')
args = parser.parse_args()

directory_video = Path('/home/pat/Videos/')
tv_directory = Path('/home/pat/NAS/TV/')
# test settings
#directory_video = Path('/home/pat/video_test/')
#tv_directory = Path('/home/pat/Videos/')

def generate(episodes):
    '''input: list of episodes on each disc
    output: dictionary with keys that are disc numbers and
    values of matching strings for episodes on each disc
    '''
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

def s_g_d(directory, episodes, start):
    '''grabs folder name, seperates out relevant info, generates new filenames,
    replaces old filenames with new'''
    # grab folder name
    for filename in sorted(directory.iterdir()):
        path_show = filename
        break
    # grab show name from folder name
    # grab season from folder name
    path_show = path_show.stem
    show_name = re.split(r'_S\d', path_show)[0]
    # create folder on server if needed
    try:
        os.mkdir(tv_directory.joinpath(show_name))
    except FileExistsError:
        pass
    #j = 0
    i = start
    paths =[]
    # loop through each disc folder, low to high
    for directory_name in sorted(directory.iterdir()):
        os.chdir(directory_name)
        season_number = directory_name.as_posix()[-3]
        # loop through each file in folder, low to high
        for filename in sorted(Path.cwd().iterdir()):
            #create new file name
            new_path = Path(show_name +'_S' + season_number + 'E' + str(i) + '.mkv')
            # rename each file, then move
            os.rename(filename, new_path)
            os.chmod(new_path, 0o444)
            print('Transferring file {}'.format('S' + season_number + 'E' + str(i)))
            shutil.move(new_path,tv_directory.joinpath(show_name,new_path))
            print('Finished Transferring file {}'.format('S' + season_number + 'E' + str(i)))
            #paths.append(show_list[j])
            paths.append(new_path)
            #if j == episodes:
            #    break
            if i == episodes:
                break
            #j += 1
            i += 1
    return paths, path_show

episode_list = args.episodes_per_disc
# runs generate to create dictionary for what to find and replace
if args.many_per_file:
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
    try:
        os.mkdir(tv_directory+path_show)
    except  FileExistsError:
        pass
    # move files
    for path in paths_discs_new:
        shutil.move(path,tv_directory+path_show+'/'+path.name)
elif args.one_per_file:
    episodes = 0
    for i in episode_list:
        episodes += int(i)
    paths, path_show = s_g_d(directory_video, episodes, args.start)
else:
    print('need to know how many episodes per file')
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
