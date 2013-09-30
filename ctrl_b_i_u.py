"""
Commands to go with keybindings in @settings-->@keys-->@shortcuts
to implement Ctrl-B,I,U Bold Italic Underline markup in plain text.
RST flavored, could be made language aware.

Key bindings would be something like:

markup_inline_bold ! body = Ctrl-B
markup_inline_italic ! body = Ctrl-I
markup_inline_underline ! body = Ctrl-U

"""

def markup_inline(kw, kind='unknown'):

    c = kw['c']
    
    # find out if last action was open or close, creates entry if needed
    last_type = c.user_dict.setdefault(
        'markup_inline', {'last': 'close'})['last']
    
    p = c.p
    
    delim = {
        'bold': ('**','**'),
        'italic': ('*','*'),
        'underline': (':ul:`','`'),
    }[kind]
    
    if c.frame.body.bodyCtrl.hasSelection():
        c.user_dict['markup_inline']['last'] = 'close'
        i,j = c.frame.body.bodyCtrl.getSelectionRange()
        txt = c.frame.body.bodyCtrl.getAllText()
        p.b = "".join([
            txt[:i],
            delim[0],
            txt[i:j],
            delim[1],
            txt[j:],
        ])
        c.frame.body.bodyCtrl.setAllText(p.b)
        c.frame.body.bodyCtrl.setInsertPoint(j+len(delim[0])+len(delim[1]))
    else:
        i = c.frame.body.bodyCtrl.getInsertPoint()
        txt = c.frame.body.bodyCtrl.getAllText()
        if last_type == 'close':
            delim = delim[0]
            c.user_dict['markup_inline']['last'] = 'open'
        else:
            delim = delim[1]
            c.user_dict['markup_inline']['last'] = 'close'
        p.b = "".join([
            txt[:i],
            delim,
            txt[i:]
        ])
        c.frame.body.bodyCtrl.setAllText(p.b)
        c.frame.body.bodyCtrl.setInsertPoint(i+len(delim))
    c.setChanged(True)
    p.setDirty(True)
    c.redraw()
    c.bodyWantsFocusNow()        

@g.command('markup_inline_bold')
def markup_inline_bold(kw):
    markup_inline(kw, kind='bold')

@g.command('markup_inline_italic')
def markup_inline_bold(kw):
    markup_inline(kw, kind='italic')

@g.command('markup_inline_underline')
def markup_inline_bold(kw):
    markup_inline(kw, kind='underline')

