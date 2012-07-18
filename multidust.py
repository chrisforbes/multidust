#!/usr/bin/env python2

# multidust -- compile multiple dust templates from one file.
# templates are named by {!name!} at the start of a line

# usage:
#     $ multidust.py FILES > templates.js

# capture stdout to some .js
# let stderr spew, you want the errors if there are any.

# blame for this atrocity:
#     chrisf@catalyst.net.nz

import re
import sys
from subprocess import Popen, PIPE

lines = []
name = None

def emit_template():
    global name, lines
    if name is not None and len(lines):
        p = Popen(['dustc', '-n='+name, '-'], stdin=PIPE)
        for l in lines:
            p.stdin.write(l)
        p.stdin.close()
        p.wait()
        print ''
    name = None
    lines = []

for f in sys.argv[1:]:
    for l in open(f,'r').readlines():
        m = re.search('^{!([^!}]+)!}$', l)
        if m != None:
            template_name = m.group(1)
            if ' ' in template_name:
                continue
            emit_template()
            name = template_name
        else:
            lines.append(l)

    emit_template()
