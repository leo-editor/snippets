import time
import base64
import textwrap

p = c.p
if not p.h.startswith('@bk '):
    nd = p.insertAfter()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    nd.h = "@bk %s %s" % (p.h, ts)
    s = '\n'.join(textwrap.wrap(
        base64.b64encode(p.b),
        break_long_words=True
    ))
    nd.b = "# backup %s - %s\n\n%s" % (ts, p.h, s)
    c.redraw()
    c.bodyWantsFocusNow()
    
else:
    
    hdr, s = p.b.split('\n', 1)
    if hdr.startswith("# backup"):  # decode
        hdr = hdr.replace('backup', 'BACKUP')
        p.b = "%s\n\n%s" % (
            hdr,
            base64.b64decode(s.strip())
        )
        
    else:  # encode again
        hdr = hdr.replace('BACKUP', 'backup')
        s = '\n'.join(textwrap.wrap(
            base64.b64encode(s.strip()),
            break_long_words=True
        ))
        p.b = "%s\n\n%s" % (hdr, s)
        
    c.redraw()
    c.frame.body.setInsertPoint(0)
    c.bodyWantsFocusNow()
