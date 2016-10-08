#! /usr/bin/env python
import os, sys
queue = []
def write(*args):
    sys.stdout.write(*args)
    sys.stdout.flush()
def tput(*args):
    os.system('tput ' + ''.join([str(i) for i in args]))
def color(c):
    queue.append(c)
def group(a, b):
    for c in range(a, b + 1):
        color(c)
def gline(*args):
    group(*args)
    flush()
def space(n=1):
    for i in range(n):
        queue.append(' ')
def newline():
    tput('sgr0')
    write('\n')
def cflush(c, cmd):
    tput('sgr0')
    if c == ' ':
        write('    ')
    else:
        tput(cmd + ' ', c)
        write('%4i' % c if cmd == 'setaf' else '    ')
def flush():
    global queue
    for c in queue:
        cflush(c, 'setaf')
    newline()
    for c in queue:
        cflush(c, 'setab')
    newline()
    queue = []
group(0,7)
space()
gline(8, 15)

for i in range(16, 231, 12):
    group(i, i + 5)
    space(3)
    gline(i + 6, i + 11)
gline(232, 243)
gline(244, 255)

#for i in range(16):
#    for j in range(16):
#        c = 16 * i + j
#        os.system('tput setaf %i' % c)
#        sys.stdout.write('%4i' % c)
#        sys.stdout.flush()
#    print('')
#os.system('tput sgr0')
