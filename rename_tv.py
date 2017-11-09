#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 18:18:53 2017

@author: pat
Require python 3.6 for os functions
"""
import os

# os.getcwd()
directory = '/home/pat/Videos/'


def generate(*episodes):
    '''input: comma seperarted list of episodes on each disc
    output: dictionary with keys that are disc numbers and
    values of matching strings for episodes on each disc'''

    targets = {}
    n = 1
    m = 0
    l = 1
    k = episodes[m] + 1
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
        k = episodes[m] + l
        n += 1
    return targets


def s_a_d(directory, targets):
    '''finds keys of targets and replaces keys with values in selected text'''
    with os.scandir(directory) as i:
        for filename in i:
            # rename files (ignoring file extensions)
            # filename and extensionname (extension in [1])
            filename_split = os.path.splitext(filename)
            filename_zero = str(filename_split[0])
            extension = str(filename_split[1])
            for j in targets.keys():
                if j in filename_zero:
                    path1 = os.path.join(filename)
                    path2 = os.path.join(filename_zero.replace(j, targets.get(j) + extension))
                    os.rename(path1, path2)
    return(path1, path2)
# create folder on server and/or move files in folder to server
# def
# runs generate to create dictionary for what to find and replace
dict = generate(8, 7, 7)

# feed directory and dictionary to s_a_d function
#s_a_d(directory, dict)
# create folder on server and/or move files in folder to server
    # try mkdir()
    # except  FileExistsError:
        #    break
# update kodi database
# check database and remove files from wanted list
