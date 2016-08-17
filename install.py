#!/usr/bin/env python
from sys import argv
from os import listdir, symlink
from os.path import (
    abspath,
    dirname,
    exists,
    expanduser,
    isdir,
    isfile,
    join,
    realpath,
)

cur_path = abspath(dirname(__file__))
home_path = expanduser('~')
assert isdir(cur_path)
assert isdir(home_path)

with open(join(cur_path, 'dotfile_blacklist.txt')) as f:
    blacklist = f.read().replace('\r', '').split('\n')
    blacklist = list(filter(bool, blacklist))

for dotfile in listdir(cur_path):
    if dotfile.startswith('.') and isfile(dotfile) and dotfile not in blacklist:
        full_path = join(cur_path, dotfile)
        dest_path = join(home_path, dotfile)
        if isfile(dest_path):
            if realpath(dest_path) != realpath(full_path):
                if dest_path == realpath(dest_path):
                    print('Error: Not linking %s: already exists' % dotfile)
                else:
                    print('Error: Not linking %s: already linked to %s' % (dotfile, realpath(dest_path)))
        elif exists(dest_path):
            print('Error: Not linking %s: already exists and is not a file' % dotfile)
        else:
            print('Linking %s' % dotfile)
            symlink(full_path, dest_path)
