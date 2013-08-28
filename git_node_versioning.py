from leo.extensions import sh
import binascii

GIT_DIR = "/home/tbrown/r/gittest/.git"

hooks = 'select2', 'unselect2', 'save1', 'end1'

if hasattr(c, 'node_change'):
    for i in hooks:
        try:
            g.unregisterHandler(i, c.node_change)
        except TypeError:
            pass  # happens if it wasn't registered

def do_git(cmd, _in=None):
    
    # print cmd    
    cmd = ["--git-dir=%s"%GIT_DIR] + cmd.split()
    
    if _in is not None:
        return sh.git(cmd, _in=_in)
    else:
        return sh.git(cmd)

def node_change(tag, kwargs):
    
    # print tag
    
    if tag == 'select2':
        v = kwargs['new_p'].v
        v._init = (v.h, v.b)
        return
        
    if tag == 'end1':
        p = c.p
    elif tag == 'save1':
        p = kwargs['p']
    elif tag == 'unselect2':
        p = kwargs['old_p']
    else:
        raise Exception("Unknown hook")
        
    v = p.v
        
    if v._init != (v.h, v.b):

        node_data = "%s\n%s" % (v.h, v.b)
        
        # get previous HEAD
        try:
            head = do_git('rev-parse HEAD')
        except sh.ErrorReturnCode:
            head = None
        
        # get hash for data
        obj = do_git("hash-object -w --stdin", _in=node_data)
                     
        # add path using gnx as a path
        do_git("update-index --add --cacheinfo 100755 %s %s" % (
               obj, v.gnx))

        # add path using UNL as a path
        # have to use hex to make path safe for git
        safe_path = binascii.b2a_hex(p.get_UNL(with_file=False))
        do_git("update-index --add --cacheinfo 100755 %s %s" % (
               obj, safe_path))

        # make a tree object from index        
        tree = do_git("write-tree")
        
        # commit tree object
        cmd = "commit-tree %s" % tree
        if head:
            cmd = "%s -p %s" % (cmd, head)
        commit = do_git(cmd, _in=c.fileName())
        
        # update HEAD
        do_git("reset %s" % commit)  
        
        # in case we were triggered by save1 or a explicit commit command  
        v._init = (v.h, v.b)

c.node_change = node_change
for i in hooks:
    g.registerHandler(i, c.node_change)
c.node_change('select2', dict(c=c, new_p=c.p, old_p=c.p, new_v=c.p.v, old_v=c.p.v))

