#! /usr/bin/env python
import argparse, fnmatch, os, subprocess, sys, time

NO_COLOR = False
if '--no-color' in sys.argv:
    sys.argv.remove('--no-color')
    NO_COLOR = True
if not sys.stdout.isatty() or not sys.stderr.isatty():
    NO_COLOR = True

def hex2rgb(s):
    s = s.replace('#', '')
    if len(s) not in (3, 6):
        raise ValueError('Invalid hexadecimal color')
    if len(s) == 3:
        s = ''.join([2 * s[i] for i in range(3)])
    return tuple([int(s[i:i+2], 16) for i in range(0, 6, 2)])

def hex2rgb_check(s):
    try:
        return hex2rgb(s)
    except ValueError:
        raise ValueError('Invalid hex color: %r' % s)

def rgb2hex(rgb):
    if len(rgb) != 3:
        raise ValueError('Invalid RGB color')
    return ''.join([hex(int(max(0, min(255, x))))[2:].zfill(2) for x in rgb])

def rgb2applescript(rgb):
    if len(rgb) != 3:
        raise ValueError('Invalid RGB color')
    return '{%i, %i, %i, 0}' % tuple([max(0, min(255, x)) * 256 for x in rgb])

def clean_hostname(host):
    # strip user from host
    return host.split('@')[-1]

def parse_ssh_config():
    # returns a list of (host, key, value) tuples
    config = []
    cur_hosts = tuple()
    config_path = os.path.expanduser('~/.ssh/config')
    if not os.path.isfile(config_path):
        print('color-ssh: %s: not found' % config_path)
        return config
    with open(config_path) as f:
        for line_id, line in enumerate(f.readlines()):
            line = line.split()
            if not line:
                continue
            line[0] = line[0].lower()
            if line[0] == 'host':
                cur_hosts = tuple(line[1:])
            else:
                for host in cur_hosts:
                    config.append((host, line[0], line[1]))
    return config

def apply_ssh_config(config, hostname):
    out = {}
    for host, key, value in config:
        if fnmatch.fnmatch(hostname, host) and not key.lower() in out:
            out[key.lower()] = value
    return out

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

in_test = False
ssh_config = parse_ssh_config()
base_config = apply_ssh_config(ssh_config, '*')

if len(sys.argv) >= 2:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('host')
    parser.add_argument('test_host', nargs='?')
    for arg_opt in 'bcDEeFIiJLlmOopQRSWw':
        parser.add_argument('-' + arg_opt)
    for no_arg_opt in '46AaCfGgKkMNnqsTtVvXxYy':
        parser.add_argument('-' + no_arg_opt, action='store_true')
    args, unknown = parser.parse_known_args()

    host = args.host
    test_host = base_config.get('#color.test', 'test')
    if host == test_host:
        in_test = True
        if args.test_host is None:
            sys.stderr.write('color-ssh: test mode requires a host or arguments\n')
            exit()
        host = args.test_host
        if NO_COLOR:
            sys.stderr.write('color-ssh: Color is disabled.\n')
            sys.stderr.flush()
        else:
            print('Testing SSH color. Press Ctrl-C to exit.')

    host = clean_hostname(host)
    host_config = apply_ssh_config(ssh_config, host)
    if '#color' in host_config:
        terminal.color(hex2rgb_check(host_config['#color']))

def run_script(p):
    p = os.path.expanduser(p)
    if os.path.exists(p):
        try:
            subprocess.call(['sh', p] + sys.argv[1:])
        except subprocess.CalledProcessError:
            pass

run_script('~/.bash/color-ssh-pre.sh')

exit_code = 0
try:
    if in_test:
        # should be long enough
        time.sleep(120)
    else:
        exit_code = subprocess.call(['ssh'] + sys.argv[1:])
except:
    print('\n')
finally:
    terminal.color(hex2rgb_check(base_config.get('#color.base', '#888888')))

run_script('~/.bash/color-ssh-post.sh')
exit(exit_code)
