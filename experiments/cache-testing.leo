<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="vitalije.20170813190447.2"><vh>About this file</vh></v>
<v t="vitalije.20170813190531.1"><vh>test createOutlineFromCacheList @key=Alt-4</vh>
<v t="vitalije.20170813190531.2"><vh>test_node</vh></v>
<v t="vitalije.20170813200848.1"><vh>tuplifyCacheList</vh></v>
<v t="vitalije.20170813200005.1"><vh>make_outline_clone_1</vh></v>
<v t="vitalije.20170813200001.1"><vh>add_extra_node_to_cache_list</vh></v>
<v t="vitalije.20170813195958.1"><vh>make_outline_clone_2</vh></v>
<v t="vitalije.20170813200023.1"><vh>make_outline_clone_3</vh></v>
<v t="vitalije.20170813200158.1"><vh>make_outline_clone_4</vh></v>
<v t="vitalije.20170813203858.1"><vh>newgnx</vh></v>
<v t="vitalije.20170813203113.1"><vh>clear gnxDict</vh></v>
<v t="vitalije.20170813202840.1"><vh>recreate_node</vh></v>
<v t="vitalije.20170813202856.1"><vh>test1</vh></v>
<v t="vitalije.20170813202902.1"><vh>test2</vh></v>
<v t="vitalije.20170813204046.1"><vh>test3</vh></v>
<v t="vitalije.20170813204232.1"><vh>test4</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="vitalije.20170813190447.2">This file is meant to be a workbook for developing tests for
leoCache module.

I suspect that not all cases are considered when recreating clones
from cache. There are following cases that need to be tested:

    1. clone in cache has children with the same gnxes as clone in outline
    2. clone in cache has at least one child that clone in outline hasn't
    3. clone in outline has at least one child than clone in cache hasn't
    4. clone in cache has at least one child that clone in outline hasn't and
       clone in outline has at least one child that clone in cache hasn't</t>
<t tx="vitalije.20170813190531.1" line_numbering_root="4930310a2e">from contextlib import contextmanager
import leo.core.leoNodes as leoNodes
import pprint
@others
c.frame.log.selectTab('Log')
c.frame.log.clearLog()
test1(False)
test2(False)
test3(False)
test4(True)</t>
<t tx="vitalije.20170813190531.2">@contextmanager
def test_node(h, keep_node=False):
    p2 = c.p.copy()
    p1 = c.lastTopLevel().insertAfter()
    p1.h = h
    try:
        c.redraw()
        yield p1.copy()
    except Exception as e:
        g.es_error(e)
    finally:
        clearGnxDict()
        if not keep_node:
            p1.doDelete(p2)
        c.selectPosition(p2)
        c.redraw()</t>
<t tx="vitalije.20170813195958.1">def make_outline_clone_2(p):
    p1, cList = make_outline_clone_1(p)
    add_extra_node_to_cache_list(cList, newgnx(), 'extra', 'extra node in cache')
    return p1, cList</t>
<t tx="vitalije.20170813200001.1">def add_extra_node_to_cache_list(aList, gnx, h, b):
    aList2 = aList[-1]
    aList2.append([h, b, gnx, []])</t>
<t tx="vitalije.20170813200005.1">def make_outline_clone_1(p):
    '''creates subtree like this:
        --C
           --A
           --B
        and returns (C-position, cache list)
    '''
    p1 = p.insertAsLastChild()
    p1.h = 'C'
    p1.b = 'outline clone'
    cgnx = p1.gnx
    p2 = p1.insertAsLastChild()
    p2.h = 'A'
    p2.b = 'node A'
    p3 = p1.insertAsLastChild()
    p3.h = 'B'
    p3.b = 'node B'
    return p1, c.cacher.makeCacheList(p1)</t>
<t tx="vitalije.20170813200023.1">def make_outline_clone_3(p):
    p1, cList = make_outline_clone_1(p)
    aList = cList[-1]
    aList.pop()
    return p1, cList
</t>
<t tx="vitalije.20170813200158.1">def make_outline_clone_4(p):
    '''creates subtree like this:
        --C
           --A
           --B
           --E
        and returns (C-position, cache list adjusted)
    '''
    p1 = p.insertAsLastChild()
    p1.h = 'C'
    p1.b = 'outline clone'
    cgnx = p1.gnx
    p2 = p1.insertAsLastChild()
    p2.h = 'A'
    p2.b = 'node A'
    p3 = p1.insertAsLastChild()
    p3.h = 'B'
    p3.b = 'node B'
    cList = c.cacher.makeCacheList(p1)
    cList[-1].append(['D', 'extra node in cache', newgnx(), []])
    p4 = p1.insertAsLastChild()
    p4.h = 'E'
    p4.b = 'extra node in outline'
    return p1, cList</t>
<t tx="vitalije.20170813200848.1">def tuplifyCacheList(aList):
    h, b, gnx, childList = aList
    children = tuple(tuplifyCacheList(x) for x in childList)
    return (h, b, gnx, children)</t>
<t tx="vitalije.20170813202840.1">def recreate_node(p, aList):
    aList1 = ['...', '', p.gnx, [aList]]
    c.cacher.createOutlineFromCacheList(p.v, aList1, 'dummy-file')
    aList2 = c.cacher.makeCacheList(p.firstChild())
    return p.firstChild(), tuplifyCacheList(aList2)</t>
<t tx="vitalije.20170813202856.1">def test1(keep_node):
    with test_node('Case 1', keep_node) as p:
        p1, cList = make_outline_clone_1(p)
        v1_data = tuplifyCacheList(cList)
        p2, v2_data = recreate_node(p.insertAsLastChild(), cList)
        if v1_data != v2_data:
            g.es(pprint.pformat(v1_data) + '\n!=\n' + pprint.pformat(v2_data))
            assert False, 'case_1 failed'
        else:
            g.es('case 1: ok')</t>
<t tx="vitalije.20170813202902.1">def test2(keep_node):
    with test_node('Case 2', keep_node) as p:
        p1, cList = make_outline_clone_2(p)
        v1_data = tuplifyCacheList(cList)
        p2, v2_data = recreate_node(p.insertAsLastChild(), cList)
        if v1_data != v2_data:
            g.es(pprint.pformat(v1_data) + '\n!=\n' + pprint.pformat(v2_data))
            assert False, 'case_2 failed'
        else:
            g.es('case 2: ok')</t>
<t tx="vitalije.20170813203113.1">def clearGnxDict():
    a = set(v.gnx for v in c.all_unique_nodes())
    b = set(c.fileCommands.gnxDict.keys())
    n = len(b - a)
    for gnx in (b - a):
        del c.fileCommands.gnxDict[gnx]
    if n &gt; 0:
        g.es('cleared %d nodes'%n)</t>
<t tx="vitalije.20170813203858.1">NI = g.app.nodeIndices
def newgnx():
    t_s = NI.update()
    return g.toUnicode("%s.%s.%d" % (NI.userId, t_s, NI.lastIndex))</t>
<t tx="vitalije.20170813204046.1">def test3(keep_node):
    with test_node('Case 3', keep_node) as p:
        p1, cList = make_outline_clone_3(p)
        v1_data = tuplifyCacheList(cList)
        p2, v2_data = recreate_node(p.insertAsLastChild(), cList)
        if v1_data != v2_data:
            g.es(pprint.pformat(v1_data) + '\n!=\n' + pprint.pformat(v2_data))
            assert False, 'case_3 failed'
        else:
            g.es('case 3: ok')</t>
<t tx="vitalije.20170813204232.1">def test4(keep_node):
    with test_node('Case 4', keep_node) as p:
        p1, cList = make_outline_clone_4(p)
        v1_data = tuplifyCacheList(cList)
        p2, v2_data = recreate_node(p.insertAsLastChild(), cList)
        if v1_data != v2_data:
            g.es(pprint.pformat(v1_data) + '\n!=\n' + pprint.pformat(v2_data))
            assert False, 'case_4 failed'
        else:
            g.es('case 4: ok')</t>
</tnodes>
</leo_file>
