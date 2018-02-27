"""
switch between code and test

https://docs.pytest.org/en/latest/

If you're using `pytest` and use the layout described below, this @button code
will jump you between a function and its test, creating the (text)function
if it doesn't already exist.  Also the tests folder and `test_foo.py` file.
It assumes use of the `active_path` plugin which headlines folders are
`/myFolder/` with body text `@path myFolder`.
"""

import re
tests_path = c.config.getString("pytest-path") or "tests"
info = {}
for nd in p.self_and_parents_iter():
    definition = re.match(r'def ([^( ]*)\(', p.b)
    if definition and not info.get('func'):
        info['func'] = definition.group(1)
    if nd.h.endswith('.py') and not info.get('file'):
        info['file'] = nd.h.split()[-1].split('/')[-1]
    if nd.h.strip('/') == tests_path.strip('/'):
        info['test'] = True

nd = p.copy()

if info.get('test'):
    while nd.h.strip('/') != tests_path.strip('/'):
        nd = nd.parent()
    if info.get('file'):
        target = info['file'][5:]
        for sib in nd.self_and_siblings():
            if sib.h.endswith(target):
                nd = sib
                break
        else:
            nd = nd.insertAfter()
            nd.h = '@auto ' + target
    if info.get('func'):
        target = info['func'][5:]
        for child in nd.children():
            if child.h == target:
                nd = child
                break
        else:
            nd = nd.insertAsLastChild()
            nd.h = target
            nd.b = 'def'  # let abbreviation build the rest
else:
    if info.get('func'):
        nd.moveToParent()
    for sib in nd.self_and_siblings():
        if sib.h.strip('/') == tests_path.strip('/'):
            nd = sib
            break
    else:
        nd = nd.insertBefore()
        nd.h = "/%s/" % tests_path.strip('/')
        nd.b = "@path %s" % tests_path
    if info.get('file'):
        target = 'test_' + info['file']
        for child in nd.children():
            if child.h.endswith(target):
                nd = child
                break
        else:
            nd = nd.insertAsLastChild()
            nd.h = "@auto %s" % target
            nd.b = "import %s\n\n@others\n" % info['file'].replace('.py', '')
    if info.get('func'):
        target = 'test_' + info['func']
        for child in nd.children():
            if child.h == target:
                nd = child
                break
        else:
            nd = nd.insertAsLastChild()
            nd.h = target
            nd.b = "def %s():\n    assert %s. == 'otters'\n" % (
                target, info['file'].replace('.py', ''))

c.selectPosition(nd)
c.redraw()
