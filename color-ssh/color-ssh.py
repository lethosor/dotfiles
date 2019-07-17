#! /usr/bin/env python
import argparse, collections, fnmatch, os, shlex, subprocess, sys, time
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
    return ''.join([hex(int(max(0, min(255, x))))[2:].zfill(2) for x in rgb])

def rgb2applescript(rgb):
    if len(rgb) != 3:
        raise ValueError('Invalid RGB color')
    return '{%i, %i, %i, 0}' % tuple([max(0, min(255, x)) * 256 for x in rgb])

def parse_ssh_config():
    config = collections.OrderedDict()
    cur = None
    config_path = os.path.expanduser('~/.ssh/config')
    if not os.path.isfile(config_path):
        print('color-ssh: %s: not found' % config_path)
        return config
    with open(config_path) as f:
        for line in f.readlines():
            line = line.split()
            if not line or line[0].startswith('#'):
                continue
            line[0] = line[0].lower()
            if line[0] == 'host':
                cur = {}
                for host in line[1:]:
                    config[host] = cur
            elif cur is None:
                raise ValueError('color-ssh: %s: line %r found before host' %
                    (config_path, line))
            else:
                cur[line[0]] = line[1]
    return config

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
        sys.stdout.write('\033]11;#%s\007' % rgb2hex(rgb))
        sys.stdout.flush()

    def color_apple(self, rgb):
        subprocess.call(['osascript', '-e',
            'tell application "Terminal" to set background color of '
            'every tab of every window whose tty is "%s" to %s'
            % (os.ttyname(sys.stdout.fileno()), rgb2applescript(rgb))])
    color_Apple_Terminal = color_apple

    def color_iterm(self, rgb):
        sys.stdout.write('\033]Ph%s\033\\' % rgb2hex(rgb))
        sys.stdout.flush()

if 'COLOR_SSH_TERM' in os.environ:
    terminal = Terminal(os.environ['COLOR_SSH_TERM'])
elif 'SSH_TTY' in os.environ or 'SSH_CLIENT' in os.environ:
    terminal = Terminal('ssh')
elif 'XTERM_VERSION' in os.environ:
    terminal = Terminal('xterm')
elif os.environ.get('TERM_PROGRAM', '') == 'Apple_Terminal':
    terminal = Terminal('apple')
elif os.environ.get('TERM_PROGRAM', '').lower().startswith('iterm'):
    terminal = Terminal('iterm')
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
            if parts[0].startswith('@'):
                config[parts[0]] = parts[1]
            else:
                config[parts[0]] = hex2rgb(parts[1])
        except ValueError:
            sys.stderr.write("%s: Invalid color at line %i\n" % (config_path, line_id))
            continue

if not '*' in config:
    config['*'] = hex2rgb('#ffffaf')
if not '<default>' in config:
    config['<default>'] = hex2rgb('#ffffff')
in_test = False
if len(sys.argv) >= 2:
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('test_host', nargs='?')
    for arg_opt in 'bcDEeFIiJLlmOopQRSWw':
        parser.add_argument('-' + arg_opt)
    for no_arg_opt in '46AaCfGgKkMNnqsTtVvXxYy':
        parser.add_argument('-' + no_arg_opt, action='store_true')
    args, unknown = parser.parse_known_args()

    host = args.host
    test_host = config.get('@test', 'test')
    if host == test_host:
        in_test = True
        if args.test_host is None:
            sys.stderr.write('color-ssh: test mode requires a host or arguments\n')
            exit()
        host = args.test_host
        print('Testing SSH color. Press Ctrl-C to exit.')
    elif unknown:
        print('color-ssh: warning: unrecognized arguments: ' + ', '.join(unknown))

    # Check whether this host is an alias defined in ~/.ssh/config
    ssh_config = parse_ssh_config()
    if host in ssh_config and 'hostname' in ssh_config[host]:
        host = ssh_config[host]['hostname'].replace('%h', host)
    else:
        # Check for wildcard hostname matches
        for host_pattern, host_config in ssh_config.items():
            if fnmatch.fnmatch(host, host_pattern):
                if 'hostname' in host_config:
                    host = host_config['hostname'].replace('%h', host)

    for k in config:
        if fnmatch.fnmatch(host, k):
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
    if in_test:
        # should be long enough
        time.sleep(120)
    else:
        subprocess.call(['ssh'] + sys.argv[1:])
except:
    print('\n')
finally:
    terminal.color(config['<default>'])

run_script('~/.bash/color-ssh-post.sh')
