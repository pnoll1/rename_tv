# rename_tv
Program is used to rewrite file names so Kodi will index properly.

input:comma seperated values of episodes per disc and disc image files in directory
output: renamed files

example:
- change directory to direrctory where files are: /home/user/Videos
- check disc images are named show_s1d1, show_s2d2 etc.
- feed values to generate:  generate(8,7,7)
- replace file names with newly generated: s_a_d(directory,dict)
- output: show_s1e01_02_03_04_05_06_07_08,show_s1e09_10_11_12_13_14_15 etc.
