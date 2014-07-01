# execute code after typing has not happened for a while

import time
hooks = ['bodykey2', 'idle']
if hasattr(c, '_typing_idle'):
    # if this code is being run a second time, drop previous handler
    g.unregisterHandler(hooks, c._typing_idle['handler'])
else:
    # execute in 5 sec. from now, create a "namespace" c._typing_idle
    # for out (two) variables
    c._typing_idle = {'next': time.time() + 5}

def handler(tag, kwargs, c=c):
    
    # wrong outline, ignore
    if kwargs['c'] != c:
        return
    
    # defer 5 more sec.
    if tag == 'bodykey2':
        c._typing_idle['next'] = time.time() + 5
        return

    # must be the idle hook, see if it's time to fire
        
    if time.time() >= c._typing_idle['next']:
        # wait for another keystroke or 5 million seconds
        c._typing_idle['next'] = time.time() + 5000000
        
        # code to do stuff here
        g.es('do stuff')

# keep a reference to the handler function
c._typing_idle['handler'] = handler
g.registerHandler(hooks, c._typing_idle['handler'])
