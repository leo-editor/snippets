from leo.extensions import sh
from leo.extensions.sh import git
import binascii

GIT_DIR = "/home/tbrown/r/gittest/.git"

git = git.bake(git_dir=GIT_DIR)

hooks = 'select2', 'unselect2', 'save1', 'end1', 'after-create-leo-frame'

if hasattr(c, 'node_change'):
    for i in hooks:
        try:
            g.unregisterHandler(i, c.node_change)
        except TypeError:
            pass  # happens if it wasn't registered

def node_change(tag, kwargs):

    if tag in ('select2', 'after-create-leo-frame'):
        v = kwargs['c'].p.v
        v._init_content = (v.h, v.b)
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
    
    if not hasattr(v, '_init_content'):
        return
        
    if v._init_content != (v.h, v.b):

        node_data = "%s\n%s" % (v.h, v.b)
        
        # get previous HEAD
        try:
            head = git('rev-parse', 'HEAD').strip()
        except sh.ErrorReturnCode:
            head = None
        
        # get hash for data, and save data in db
        obj = git('hash-object', '-w', '--stdin', _in=node_data).strip()
                     
        # add path using gnx as a path
        git('update-index', '--add', '--cacheinfo', '100755', obj, v.gnx)

        # add path using UNL as a path
        # have to use hex to make path safe for git
        safe_path = binascii.b2a_hex(p.get_UNL(with_file=False))
        git('update-index', '--add', '--cacheinfo', '100755', obj, safe_path)

        # make a tree object from index        
        tree = git("write-tree").strip()
        
        # commit tree object
        cmd = ['commit-tree', tree]
        if head:
            cmd += ['-p', head]
        commit = git(cmd, _in=p.get_UNL()).strip()

        # update HEAD
        git('reset', commit)  
        
        # in case we were triggered by save1 or a explicit commit command  
        v._init_content = (v.h, v.b)

c.node_change = node_change
for i in hooks:
    g.registerHandler(i, c.node_change)
c.node_change('select2', dict(c=c, new_p=c.p, old_p=c.p, new_v=c.p.v, old_v=c.p.v))
