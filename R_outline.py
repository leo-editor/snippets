# insert / update headlines as comments in @nosent R code
headlines = []
for nd in p.self_and_subtree_iter():
    
    if nd.h and nd.h[0] == '@' or nd.b and nd.b[0] == '@':
        continue
        
    headlines.append(nd.h)
    
    lines = nd.b.split('\n')
    if lines and lines[0].startswith('### '):
        del lines[0]
    if lines and lines[0].strip():
        lines[0:0] = [""]
    lines[0:0] = [
        "### %s %s" % (nd.h, "#"*(80-len(nd.h)-5)),
    ]
    if '.coffee' in p.h:
        lines[0:0] = [""]
    if lines[-1].strip():
        lines.append("")
    if lines[-2].strip():
        lines.append("")

    b = '\n'.join(lines)
    if nd.b != b:
        nd.b = b
        
g.es('\n'.join(headlines))
    
c.redraw()
