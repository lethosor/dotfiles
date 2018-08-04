#!/usr/bin/env python3
import datetime
import re
import sys

if len(sys.argv) < 2:
    raise RuntimeError('Missing filename argument')

day_delta = datetime.timedelta(days=1)

prev_date = None
with open(sys.argv[1], 'r') as f:
    # skip first line (channel name)
    f.readline()
    for line in f.readlines():
        match = re.search(r'(\d+)\-(\d+)\-(\d+)', line)
        if not match:
            raise ValueError('Could not find date')
        cur_date = datetime.datetime(*map(int, match.groups()))
        if prev_date is None:
            prev_date = cur_date
        if prev_date + day_delta < cur_date:
            print('gap: ' + prev_date.strftime('%Y-%m-%d') + ' to ' + cur_date.strftime('%Y-%m-%d'))
        prev_date = cur_date
