"""Clean up whitespace in a file"""

import re
tws = re.compile(' +\n')
hit = False
for nd in p.self_and_subtree_iter():
    t = tws.sub('\n', nd.b.rstrip(' \t\n'))+'\n\n'
    if t != nd.b:
        nd.b = t
        nd.setDirty()
        hit = True
if hit:
    c.setChanged(True)
c.redraw()
