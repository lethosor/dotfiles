#! /usr/bin/env python
import collections, fnmatch, os, shlex, subprocess, sys
config = collections.OrderedDict()
config_path = os.path.abspath(os.path.expanduser(os.environ.get('SSH_COLOR_PATH', '~/.ssh-colors.txt')))

NO_COLOR = False
if '--no-color' in sys.argv:
    sys.argv.remove('--no-color')
    NO_COLOR = True

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
        self.color = self.color_dumb
        if NO_COLOR:
            pass
        elif hasattr(self, method):
            self.color = getattr(self, method)
        else:
            sys.stderr.write('color-ssh: Unrecognized terminal: %s\n' % name)

    def color_dumb(self, rgb):
        pass

    def color_ssh(self, rgb):
        if not hasattr(self, 'color_ssh_warned'):
            self.color_ssh_warned = True
            print('color-ssh: not coloring ssh session')

    def color_xterm(self, rgb):
        sys.stdout.write('\033]11;%s\007' % rgb2hex(rgb))
        sys.stdout.flush()

    def color_apple(self, rgb):
        subprocess.call(['osascript', '-e',
            'tell application "Terminal" to set background color of first window to %s'
            % rgb2applescript(rgb)])
    color_Apple_Terminal = color_apple

if 'COLOR_SSH_TERM' in os.environ:
    terminal = Terminal(os.environ['COLOR_SSH_TERM'])
elif 'SSH_TTY' in os.environ or 'SSH_CLIENT' in os.environ:
    terminal = Terminal('ssh')
elif 'XTERM_VERSION' in os.environ:
    terminal = Terminal('xterm')
elif os.environ.get('TERM_PROGRAM', '') == 'Apple_Terminal':
    terminal = Terminal('apple')
elif os.environ.get('TERM', '').startswith('xterm'):
    terminal = Terminal('xterm')
else:
    terminal = Terminal(os.environ.get('TERM', 'dumb'))

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

def run_script(p):
    p = os.path.expanduser(p)
    if os.path.exists(p):
        try:
            subprocess.call(['sh', p] + sys.argv[1:])
        except subprocess.CalledProcessError:
            pass

run_script('~/.bash/color-ssh-pre.sh')

try:
    subprocess.call(['ssh'] + sys.argv[1:])
except:
    print('\n')
finally:
    terminal.color(config['<default>'])

run_script('~/.bash/color-ssh-post.sh')
