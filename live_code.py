"""
Proof of concept for live code in Leo, ast tree experiment

Put the this code in a node and use the script-button
button to create a button for that node.  Then put some simple code
another node, like

from math import pi
a = 10+2
a + 4
def timespi(x):
    return x*pi
timespi(a)

and use the button to run this code on that code, which executes
top level node by top level node.  Actual implementation would need
scanning from onIdle hook, keeping track of which blocks have changed,
re-calculating changed blocks and subsequent blocks, etc.

Don't run this code on its self, that would be recursive :-)
"""

import ast

source = p.b
lines = source.split('\n')

top_level = ast.parse(source)

block = []  # blocks (strings) of source code

nodes = list(ast.iter_child_nodes(top_level))

# break source up into blocks corresponding to top level nodes
for n, node in enumerate(nodes):
    if n == len(nodes) - 1:
        next_node = len(lines)
    else:
        next_node = nodes[n+1].lineno
    block.append("\n".join(lines[node.lineno-1:next_node-1]))

scope = {'p': p.copy(), 'c': c, 'g': g}

# execute blocks one by one and show results
for n, node in enumerate(nodes):
    g.es("# Block %d %s" % (n, node.__class__.__name__))
    if isinstance(node, ast.Expr):
        result = eval(block[n], scope)
        if result is not None:
            g.es(result)
    else:
        exec block[n] in scope
    if isinstance(node, ast.Assign):
        for target in node.targets:
            g.es("%s = %s" % (target.id, eval(target.id, scope)))
    if isinstance(node, ast.FunctionDef):
        g.es("function %s" % (node.name))
