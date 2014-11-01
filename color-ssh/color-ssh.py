#! /usr/bin/env python
import collections, fnmatch, os, shlex, subprocess, sys
config = collections.OrderedDict()
config_path = os.path.abspath(os.path.expanduser(os.environ.get('SSH_COLOR_PATH', '~/.ssh-colors.txt')))

def hex2rgb(s):
    s = s.replace('#', '')
    if len(s) not in (3, 6):
        raise ValueError('Invalid hexadecimal color')
    if len(s) == 3:
        s = ''.join([2 * s[i] for i in range(3)])
    return tuple([int(s[i:i+2], 16) for i in range(0, 6, 2)])

def rgb2hex(rgb):
    if len(rgb) != 3:
        raise ValueError('Invalid RGB color')
    return '#' + ''.join([hex(int(max(0, min(255, x))))[2:] for x in rgb])

def rgb2applescript(rgb):
    if len(rgb) != 3:
        raise ValueError('Invalid RGB color')
    return '{%i, %i, %i, 0}' % tuple([max(0, min(255, x)) * 256 for x in rgb])

class Terminal:
    def __init__(self, name):
        method = 'color_' + name
        if hasattr(self, method):
            self.color = getattr(self, method)
        else:
            self.color = self._color_default
            sys.stderr.write('color-ssh: Unrecognized terminal: %s\n' % name)

    def _color_default(self, rgb):
        pass

    def color_xterm(self, rgb):
        sys.stdout.write('\033]11;%s\007' % rgb2hex(rgb))
        sys.stdout.flush()

    def color_Apple_Terminal(self, rgb):
        subprocess.call(['osascript', '-e',
            'tell application "Terminal" to set background color of first window to %s'
            % rgb2applescript(rgb)])

termname = os.environ.get('TERM_PROGRAM', False) or \
            os.environ.get('TERM', '')
terminal = Terminal(termname)

if os.path.exists(config_path):
    line_id = 0
    for line in open(config_path):
        line_id += 1
        parts = shlex.split(line)
        if not len(parts) or parts[0].startswith('#'):
            continue
        if len(parts) != 2:
            sys.stderr.write("%s: Syntax error at line %i\n" % (config_path, line_id))
            continue
        try:
            config[parts[0]] = hex2rgb(parts[1])
        except ValueError:
            sys.stderr.write("%s: Invalid color at line %i\n" % (config_path, line_id))
            continue

if not '*' in config:
    config['*'] = hex2rgb('#ffffaf')
if not '<default>' in config:
    config['<default>'] = hex2rgb('#ffffff')
if len(sys.argv) >= 2:
    for k in config:
        if fnmatch.fnmatch(sys.argv[1], k):
            terminal.color(config[k])
            break

try:
    subprocess.call(['ssh'] + sys.argv[1:])
except:
    print('\n')
finally:
    terminal.color(config['<default>'])
