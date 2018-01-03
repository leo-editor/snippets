from subprocess import Popen, PIPE

# START: stuff to replace with core functions
def atfile(p):
    """Find @<file> containing p"""
    word0 = p.h.split()[0]
    return (
        word0 in g.app.atFileNames|set(['@auto']) or
        word0.startswith('@auto-')
    )

aList = g.get_directives_dict_list(p)
path = c.scanAtPathDirectives(aList)
while c.positionExists(p):
    if atfile(p):  # see if it's a @<file> node of some sort
        break
    p.moveToParent()
# END: stuff to replace with core functions

if c.positionExists(p):
    filename = g.os_path_basename(p.h.split(None, 1)[-1])
    g.es(g.os_path_join(path, filename))
    diff, err = Popen(['git', '-C', path, 'diff', filename],
        stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
    diff = diff.decode('utf-8')
    # parsing a line like `@@ -564,27 +564,27 @@ class NNNModel:`
    base = p.get_UNL(with_count=True, with_proto=True)
    for line in diff.split('\n'):
        if line.startswith('@@ '):
            # line.split()[2] would be +564,27 in the above, the modified lines
            line, lines = map(int, line.split()[2].split(','))
            g.es("%3d lines @ %d" % (lines, line),
                nodeLink="%s,%s" % (base, -(line+int(lines/2))))
            # offset to the middle of the block, -ve indicates global line num.
else:
    g.es("Didn't find file")
