# template is everything between r""" and second """
# placeholders are H heading B body C children, T ToDo priority
# use \n in B and C lines for conditional blank lines

try:
    unicode
except NameError:
    unicode = str

template = r"""T H
    B
  * C"""

lines=[]
exp_only = g.app.gui.runAskYesNoCancelDialog(
    c, 'Expanded nodes only?', 'Expanded nodes only?')
if exp_only == 'no':
    exp_only = False
    
def export_text(p, indent=''):

    spaces = u' '*(len(indent) - len(indent.lstrip(' ')))
    
    for line in template.split('\n'):
        line = unicode(line)
        if 'T' in line:
            pri = int(c.cleo.getat(p.v, 'priority') or 0)
            if pri:
                if pri <= 19:
                    if pri == 19:
                        pri = '( )'
                    else:
                        pri = '(%d)' % pri
                elif pri == 21:
                    pri = '(X)'
                elif pri == 100:
                    pri = '(/)'
                else:
                    pri = '*'
                    
            char = pri # .decode('utf-8')
            line = line.replace('T', char)
                
        if 'H' in line:
            lines.append(indent + line.replace('H', p.h))
        elif 'B' in line and p.script.strip():
            text = p.script.strip()
            prefix = line[:line.find('B')].replace('\\n', '\n')
            for i in text.split('\n'):
                lines.append(spaces + prefix + i)
                prefix = line[:line.find('B')].replace('\\n', '')
            if line.endswith('\\n'):
                lines.append('')
        elif 'C' in line and (not exp_only or p.isExpanded()):
            prefix = line[:line.find('C')].replace('\\n', '\n')
            for child in p.children():
                export_text(child, indent=spaces + prefix)
            if line.endswith('\\n'):
                lines.append('')
        elif 'C' not in line and 'B' not in line:
            lines.append(line)

if exp_only != 'cancel':
    for i in c.getSelectedPositions():
        export_text(i)
    c.leo_screen.show('\n'.join(lines), 'text', plain=True)
    
    filename = g.app.gui.runSaveFileDialog(c, 'Save to file')
    
    if filename:
        txt = '\n'.join(lines) # .encode('utf-8')
        open(filename,'w').write(txt)
