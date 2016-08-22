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

def check_existing_path(full_path, dest_path):
    if realpath(dest_path) != realpath(full_path):
        if dest_path == realpath(dest_path):
            print('Error: Not linking %s: already exists' % dotfile)
        else:
            print('Error: Not linking %s: already linked to %s' % (dotfile, realpath(dest_path)))

def link_path(full_path, dest_path):
    print('Linking %s' % dotfile)
    symlink(full_path, dest_path)


for dotfile in listdir(cur_path):
    if dotfile in blacklist:
        continue

    full_path = join(cur_path, dotfile)
    dest_path = join(home_path, dotfile)
    if dotfile.startswith('.') and isfile(dotfile):
        if isfile(dest_path):
            check_existing_path(full_path, dest_path)
        elif exists(dest_path):
            print('Error: Not linking %s: already exists and is not a file' % dotfile)
        else:
            link_path(full_path, dest_path)

    elif dotfile.endswith('.d') and isdir(dotfile):
        if isdir(dest_path):
            check_existing_path(full_path, dest_path)
        elif exists(dest_path):
            print('Error: Not linking %s: already exists and is not a directory' % dotfile)
        else:
            link_path(full_path, dest_path)
