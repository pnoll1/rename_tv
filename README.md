# rename_tv
Program is used to rewrite file names so Kodi will index properly.

input:comma seperated values of episodes per disc and disc image files in directory
output: renamed files

Usage for many per file:
1. Rip discs to directory with nothing in it and name disc files show_s1d1.iso, show_s2d2.iso etc
2. call rename_tv from command line
 - rename_tv.py --episodes-per-disc 7 8 --many-per-file
 - rename_tv.py -h to get help

usage for one per file:
1. Rip discs to video directory using Makemkv, each disc directory should be named show_s1d1, show_s1d2 etc. Files should be named title00.mkv, title 01.mkv etc. automatically by Makemkv
2. call rename_tv from command line
 - rename_tv.py --episodes-per-disc 7 8 --one-per-file --start 15
 - rename_tv.py -h to get help

Setup:
- directory_video is directory where files are ripped to
- tv_directory is where kodi tv library is located
- change url and port in requests to Kodi to your url and port

Known Limitations:
- --start only works with --one-per-file
- --many-per-file is made to handle one season at a time
