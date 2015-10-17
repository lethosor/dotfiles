#! /usr/bin/env python
import os
out = []
for p in os.environ['PATH'].split(':'):
    if p and p not in out:
        out.append(p)
print(':'.join(out))
