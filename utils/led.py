# NOTE: this is obsolete, see led.sh instead (leoremote / lproto is deprecated)

#!/usr/bin/python
"""
Load a file in a running Leo session from the command line.

The folder containing the "leo" folder has to be on the Python
path, and you need the leoremote.py plugin enabled in Leo.

usage: led [-h] [--ask] [--use USE] filename

positional arguments:
  filename    File to load

optional arguments:
  -h, --help  show this help message and exit
  --ask       Ask which Leo outline to use (default: False)
  --use USE   edit, auto, shadow, etc. for @edit etc. node (default: None)
"""

import argparse
import sys
from leo.external import lproto
import os
import time

def make_parser():
     
     parser = argparse.ArgumentParser(
         description="""Load file from command line into Leo""",
         formatter_class=argparse.ArgumentDefaultsHelpFormatter
     )
     
     parser.add_argument("--ask", action='store_true',
         help="Ask which Leo outline to use"
     )
     parser.add_argument('--use', type=str,
         help="edit, auto, shadow, etc. for @edit etc. node"
     )
     parser.add_argument('filename', type=str,
         help="File to load"
     )

     return parser
 
opt = make_parser().parse_args()
if not opt.use:
    if opt.filename.endswith(".py"):
        opt.use = 'auto'
    else:
        opt.use = 'edit'

addr = open(os.path.expanduser('~/.leo/leoserv_sockname')).read()
pc  = lproto.LProtoClient(addr)

c_n = 0  # use first commander
if opt.ask:
    pc.send("""
out = open("/tmp/clist", 'w')
for n,c in enumerate(g.app.commanders()):
    # print("%d: %s\\n"%(n,c.fileName()))
    out.write("%d: %s\\n"%(n,c.fileName()))
out.close()
""")
    time.sleep(1)  # wait for file to close - presumably pc.send()
                   # is asynchronous
    print open("/tmp/clist").read()
    
    print 'Which outline:',
    c_n = input()

pc.send("""
import os
fn = {filename!r}
c = g.app.commanders()[{which}]
h = "@{type} "+fn
n = g.findNodeAnywhere(c, h)
if not n:
    e = g.findTopLevelNode(c, 'Edits')
    if not e:
        e = c.rootPosition().insertAfter()
        e.h = 'Edits'
    n = e.insertAsNthChild(0)
    c.selectPosition(n)
    n.h = h
    c.k.simulateCommand("refresh-from-disk")
else:
    c.selectPosition(n)
c.redraw()
c.bringToFront()
""".format(
    filename=os.path.join(os.getcwd(), opt.filename),
    which=c_n,
    type=opt.use,
))
