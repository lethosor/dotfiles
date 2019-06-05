#!/usr/bin/env python

if __name__ == 'socket':
    from os import environ
    import socket_orig
    for name in dir(socket_orig):
        globals()[name] = getattr(socket_orig, name)
    _bind_orig = socket.bind

    if environ['PY_REBIND_PORTS']:
        ports_raw = environ['PY_REBIND_PORTS'].split(' ')
        ports = {int(k): int(v) for k, v in [p.split(':') for p in ports_raw]}

        def _bind_new(self, addr, *args):
            if addr[1] in ports:
                addr = (addr[0], ports[addr[1]])
            return _bind_orig(self, addr, *args)

        socket.bind = _bind_new

elif __name__ == '__main__':
    import atexit
    import os
    import re
    import shutil
    import socket
    import subprocess
    import sys
    import tempfile

    tmpdir = tempfile.mkdtemp()
    @atexit.register
    def cleanup():
        shutil.rmtree(tmpdir)

    shutil.copyfile(os.path.abspath(__file__), os.path.join(tmpdir, 'socket.py'))
    shutil.copyfile(socket.__file__, os.path.join(tmpdir, 'socket_orig.py'))

    if os.environ.get('PYTHONPATH', None):
        os.environ['PYTHONPATH'] = tmpdir + os.pathsep + os.environ['PYTHONPATH']
    else:
        os.environ['PYTHONPATH'] = tmpdir

    args = sys.argv[:]
    del args[0]  # remove executable name
    ports = []   # "original port:actual port"
    while args:
        match = re.match(r'(\d+):(\d+)', args[0])
        if match:
            ports.append(args[0])
            del args[0]
        else:
            break

    os.environ['PY_REBIND_PORTS'] = ' '.join(ports)
    subprocess.call(args)
