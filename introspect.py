@language python
"""Introspect"""

import types

sub_mode = 'instance'
# 'instance' or 'class' - controls which, instance or class names,
# are put it a subnode.  'instance class' sub-nodes both.
# '' appends classes after names, not useful.

def classname(thing):
    if hasattr(thing, '__class__'):
        return thing.__class__.__name__
    else:
        return thing.__name__

if not hasattr(c.p.v, '_introspection_target'):
    txt = g.app.gui.runAskOkCancelStringDialog(
        c, "Introspect what", "Introspect what")
    if txt is not None:
        o = eval(txt)
        c.p.v._introspection_target = o
        c.p.h = "%s %s" % (txt, classname(o))

# c.p.deletePositionsInList([i.copy() for i in p.children()])

obj = c.p.v._introspection_target
g.es(classname(obj))

def show_obj(c, obj):

    inames = sorted(dir(obj))
    
    things = {}
    instances = []
    for iname in inames:
        
        if iname.startswith('__'):
            continue
        
        o = getattr(obj, iname)
        cname = classname(o)
        instances.append((iname, o))
        things.setdefault(cname, []).append(instances[-1])

    if 'instance' in sub_mode:
        tnd = c.p.v.insertAsNthChild(0)
        tnd.h = "<by name>"
    else:
        tnd = c.p.v

    instances.sort()
    for iname, o in instances:
        
        if classname(o) == 'position':
            # apparently this collapses the space-time continuum?
            continue
        
        nd = tnd.insertAsLastChild()
        
        if not seen_already(tnd, nd, iname, o):
            nd.h = "%s %s" % (iname, format_type(nd, o))
            nd._introspection_target = o

    if 'class' in sub_mode:
        ttnd = c.p.v.insertAsNthChild(0)
        ttnd.h = "<by class>"
    else:
        ttnd = c.p.v

    for cname in sorted(things):
    
        if len(things[cname]) == 1:
            tnd = ttnd
        else:
            tnd = ttnd.insertAsLastChild()
            tnd.h = "<%s>"%cname
    
        for iname, o in sorted(things[cname]):
            
            if cname == 'position':
                # apparently this collapses the space-time continuum?
                continue
            
            nd = tnd.insertAsLastChild()
            if not seen_already(tnd, nd, iname, o):
                show_child(nd, iname, o)
                nd._introspection_target = o
         
def seen_already(tnd, nd, iname, o):
            
    for up in tnd.parents:
        if (hasattr(up, '_introspection_target') and
            getattr(up, '_introspection_target') is o):
            break
    else:
        return False
        
    nd.h = "[%s %s]" % (classname(o), iname)
    nd.b = up.get_UNL(with_file=True, with_proto=True)
    
    return True
            
def show_child(nd, iname, o):
                
    nd._introspection_target = o
    nd.h = "%s %s" % (format_type(nd, o), iname)
    
docable = (
    types.ClassType, types.MethodType, types.UnboundMethodType, 
    types.BuiltinFunctionType, types.BuiltinMethodType,
)
    
def format_type(nd, o):
    
    if isinstance(o, docable):
        if hasattr(o, '__doc__'):
            nd.b = o.__doc__
    
    if isinstance(o, (str, unicode)):
        nd.b = o
        return "%s '%s'" % (classname(o), o[:20])
    elif isinstance(o, bool):
        return "%s %s" % (classname(o), 'T' if o else 'F')
    elif isinstance(o, (int, float)):
        return "%s %s" % (classname(o), o)
    elif isinstance(o, (tuple, list, dict)):
        return "%s %s" % (classname(o), len(o))
    else:
        return classname(o)
    
def show_list(c, list_):
    
    if len(list_) > 100:
        nd = c.p.v.insertAsLastChild()
        nd.h = "<%s of %d items truncated>" % len(list_.__class__.__name__, list_)
        
    if len(list_) == 0:
        nd = c.p.v.insertAsLastChild()
        nd.h = "<%s of 0 items>" % list_.__class__.__name__
        
    for n, i in enumerate(list_[:100]):
        nd = c.p.v.insertAsLastChild()
        show_child(nd, '', i)
        nd.h = "%d: %s" % (n, nd.h)
        nd._introspection_target = i

def show_dict(c, dict_):
    
    if len(dict_) > 100:
        nd = c.p.v.insertAsLastChild()
        nd.h = "<dict of %d items truncated>" % len(dict_)
        
    if len(dict_) == 0:
        nd = c.p.v.insertAsLastChild()
        nd.h = "<dict of 0 items>"
        
    keys = dict_.keys()
    keys.sort()
        
    for k in keys[:100]:
        nd = c.p.v.insertAsLastChild()
        i = dict_[k]
        show_child(nd, '', i)
        nd.h = "%s: %s" % (k, nd.h)
        nd._introspection_target = i

dispatch = {
    list: show_list,
    tuple: show_list,
    dict: show_dict,
}

func = dispatch.get(type(obj), show_obj)

func(c, obj)
   
c.p.expand()
c.redraw()
