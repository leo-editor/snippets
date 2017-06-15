"""
Notes 2017-6-15: this is old code and may not be inserting the output
into the outline in quite the right way.

Select two nodes - click the first the ctrl-click the second.  Then run
this code.  It ignores differences in the two top nodes, but recursively
lists differences in their descendant trees.

The result tree is tagged with @bookmarks and has UNL links to the different
nodes so double clicking nodes in the result tree jumps you to the original
nodes.

A bug seems to be %20 escaping the text of differing nodes.
"""

from leo.core.leoNodes import vnode
if not hasattr(vnode, 'insertAsLastChild'):
    # add insertAsLastChild method to vnodes
    def ialc(self):
        vnode(self.context)._linkAsNthChild(self, len(self.children))
        return self.children[-1]
    vnode.insertAsLastChild = ialc

pos0, pos1 = c.getSelectedPositions()[:2]

vf = pos0.v
vt = pos1.v

nd = c.rootPosition().insertAfter()
nd.copy().back().moveAfter(nd)
nd.h = 'diff @bookmarks'

def text_match(a, b):
    return (a.h == b.h, 
            a.h == b.h and a.b == b.b)
def text_match(a, b):
    return (a.h == b.h, 
            a.h == b.h and ' '.join(a.b.split()) == ' '.join(b.b.split()))
def gnx_match(a, b):
    return (a.h == b.h and a.gnx == b.gnx, 
            a.h == b.h and a.b == b.b and a.gnx == b.gnx)

def diff_trees(vf, vt, path):

    fonly = []  # nodes only in from tree
    tonly = []  # nodes only in to tree
    diffs = []  # nodes which occur in both but have different descendants

    # count number of times each headline occurs as a child of
    # each node being compared
    count_f = {}
    for cf in vf.children:
        count_f[cf.h] = count_f.get(cf.h, 0) + 1
    count_t = {}
    for ct in vt.children:
        count_t[ct.h] = count_t.get(ct.h, 0) + 1

    for cf in vf.children:
        
        for ct in vt.children:
            
            if count_f[cf.h] == 1 and count_t[ct.h] == 1:
                equal = text_match
            else:
                equal = gnx_match
            
            head_eq, body_eq = equal(cf, ct)
            
            if body_eq:
                diffs.append(diff_trees(cf, ct, path+[vf.h]))
                
                break
            elif head_eq:
                d = diff_trees(cf, ct, path+[vf.h])
                if d:
                    d.h = '!v '+d.h
                else:
                    d = vnode(nd.v.context)
                    d.h = '!v '+cf.h
                d.b = "#%s\n\n%s" % (
                    '-->'.join((path+[vf.h]+[cf.h])[1:]),
                    cf.b
                )
                diffs.append(d)
                d = vnode(nd.v.context)
                d.h = '!^ '+cf.h
                d.b = "#%s\n\n%s" % (
                    '-->'.join((path+[vt.h]+[ct.h])[1:]),
                    ct.b
                )
                d.b = d.b.replace(' ', '%20')
                diffs.append(d)
                break
        else:
            fonly.append(cf)
            
    for ct in vt.children:
        
        for cf in vf.children:
            
            if count_f[cf.h] == 1 and count_t[ct.h] == 1:
                equal = text_match
            else:
                equal = gnx_match
            
            head_eq, body_eq = equal(cf, ct)
            if head_eq or body_eq:
                # no need to recurse matches again
                break

        else:
            tonly.append(ct)

    if not any(diffs) and not fonly and not tonly:
        return None
        
    vd = vnode(nd.v.context)
    vd.h = vf.h
    for d in diffs:
        if d:
            vd.children.append(d)
    for f in fonly:
        n = vd.insertAsLastChild()
        n.h = '- '+f.h
        n.b = "#%s" % ('-->'.join((path+[vf.h]+[f.h])[1:]))
        n.b = n.b.replace(' ', '%20')
    for t in tonly:
        n = vd.insertAsLastChild()
        n.h = '+ '+t.h
        n.b = "#%s" % ('-->'.join((path+[vf.h]+[t.h])[1:]))
        n.b = n.b.replace(' ', '%20')

    return vd

parent = c.vnode2position(vt).parent()
path = []
while parent:
    path = [parent.h] + path
    parent = parent.parent()
path = ['TOP'] + path

v = diff_trees(vf, vt, path)
if v:
    nd.v.children.extend(v.children)  # snip off <hidden root node>

c.bringToFront()
c.redraw()
