"""
switch between code and test

If you're using `pytest`[1] and use the layout described below, this @button code
will jump you between a function and its test, creating the (test)function
if it doesn't already exist.  Also the tests folder and `test_foo.py` file.
It assumes use of the `active_path` plugin which headlines folders as
`/myFolder/` with body text `@path myFolder`.

This code is very heavy on assumptions, but a lot of those are driven
by pytest default behavior.

To run tests, use `python -m pytest`, as anything involving py.test is
deprecated, and for some reason `pytest` finds files but runs no tests.
Tested with pytest 3.x, note Ubuntu 16.04 seems to still be on 2.x

Assumed layout:

/tests/
    test_utils.py
        def test_add_one()...
        def test_sub_one()...
    test_gui.py
        def test_load_buttons()...
utils.py
    def add_one()...
    def sub_one()...
gui.py
    def load_buttons()...

So running this code from a button will jump you from
test_sub_one() back to sub_one() and visa versa creating any
missing parts of the hierarchy in the process.

[1] https://docs.pytest.org/en/latest/
"""

import re
tests_path = c.config.getString("pytest-path") or "tests"
info = {}
# climb up node tree collecting info.
for nd in p.self_and_parents_iter():
    definition = re.match(r'def ([^( ]*)\(', p.b)
    if definition and not info.get('func'):
        info['func'] = definition.group(1)
    if nd.h.endswith('.py') and not info.get('file'):
        info['file'] = nd.h.split()[-1].split('/')[-1]
    if nd.h.strip('/') == tests_path.strip('/'):
        info['test'] = True

nd = p.copy()

if info.get('test'):  # we started in these tests folder
    while nd.h.strip('/') != tests_path.strip('/'):
        nd = nd.parent()  # climb up to code folder
    if info.get('file'):  # find or create code file
        target = info['file'][5:]
        for sib in nd.self_and_siblings():
            if sib.h.endswith(target):
                nd = sib
                break
        else:
            nd = nd.insertAfter()
            nd.h = '@auto ' + target
    if info.get('func'):  # find or create code function
        target = info['func'][5:]
        for child in nd.children():
            if child.h == target:
                nd = child
                break
        else:
            nd = nd.insertAsLastChild()
            nd.h = target
            nd.b = 'def'  # let abbreviation build the rest
else:  # we stared in the code folder
    if info.get('func'):  # get up to file level (weak, could be deeper)
        nd.moveToParent()
    for sib in nd.self_and_siblings():  # find or create tests folder
        if sib.h.strip('/') == tests_path.strip('/'):
            nd = sib
            break
    else:
        nd = nd.insertBefore()
        nd.h = "/%s/" % tests_path.strip('/')
        nd.b = "@path %s" % tests_path
    if info.get('file'):  # find or create test file
        target = 'test_' + info['file']
        for child in nd.children():
            if child.h.endswith(target):
                nd = child
                break
        else:
            nd = nd.insertAsLastChild()
            nd.h = "@auto %s" % target
            nd.b = "import %s\n\n@others\n" % info['file'].replace('.py', '')
    if info.get('func'):  # find or create test function
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
