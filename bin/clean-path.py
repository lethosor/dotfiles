#! /usr/bin/env python
import os
out = []
for p in os.environ['PATH'].split(':'):
    if p not in out:
        out.append(p)
print(':'.join(out))
