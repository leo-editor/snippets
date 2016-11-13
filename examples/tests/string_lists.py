import timeit

bees = [
    "[' '] * 10 + [''] + ['\\n']",
    "['', '']",
    "[' ']",
    "['']",
]

codes = [
    "bool(''.join(b))",
    "all(not i.strip() for i in b)",
    "all([not i.strip() for i in b])",
    "all(map(lambda i: not i.strip(), b))",

    "''.join(b).isspace()",
    "not all(i.isspace() for i in b)",
    "not all([i.isspace() for i in b])",
    "not all(map(lambda i: i.isspace(), b))",
]

for b in bees:
    
    g.es("\n%s" % b)
    setup = b
    b = eval(setup)
    setup = "b = " + setup
    
    for n, code in enumerate(codes):
        time = timeit.timeit(code, setup, number=100000)
        g.es("%s %5s %s" % (n, eval(code), time))
