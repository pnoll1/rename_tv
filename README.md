# rename_tv
Program is used to rewrite file names so Kodi will index properly.

input:comma seperated values of episodes per disc and disc image files in directory
output: renamed files

Usage:
1. Rip discs to directory with nothing in it and name disc files show_s1d1, show_s2d2 etc
2. call rename_tv from command line
 - rename_tv.py --episodes-per-disc 7 8 --one-per-file --start 15
 - rename_tv.py -h to get help

Setup:
- directory_video is directory where files are ripped to
- tv_directory is where kodi tv library is located
- change url and port in requests to Kodi to your url and port

Known Limitations:
- --start only works with --one-per-file
- --many-per-file
