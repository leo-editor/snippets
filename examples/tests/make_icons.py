"""
make_icons.py - make simple 4 color icons for the box00.png...box15.png

Could be adapted for other icon styles, iterates the 16 states in the
correct order.

WARNING: saves box00.png...box15.png in current directory

Terry Brown, terrynbrown@gmail.com, Tue Mar 27 12:01:11 2018
"""
from itertools import product

from PIL import Image

# ordered list of staes
states = ['clean', 'dirty'], ['no_clone', 'clone'], ['unmarked', 'marked'], ['empty', 'content']
# solarized colors
sol = {'base03': '002b36', 'base02': '073642', 'base01': '586e75', 'base00': '657b83',
    'base0': '839496', 'base1': '93a1a1', 'base2': 'eee8d5', 'base3': 'fdf6e3',
    'yellow': 'b58900', 'orange': 'cb4b16', 'red': 'dc322f', 'magenta': 'd33682',
    'violet': '6c71c4', 'blue': '268bd2', 'cyan': '2aa198', 'green': '859900'}
for k in sol:
    sol[k] = tuple([int(sol[k][i*2:i*2+2], base=16) for i in range(3)] + [255])

# states for which marks are made on the transparent icon
# pos (0,0) top left, (1,1) bottom right quarter
marks = {
    'dirty':   {'color': sol['yellow'],  'pos': (0,0)},
    'clone':   {'color': sol['magenta'], 'pos': (1,1)},
    'marked':  {'color': sol['cyan'],    'pos': (1,0)},
    'empty':   {'color': sol['base00'],  'pos': (0,1)},
}

width, height = 10, 10

for n, state in enumerate(product(*states)):
    print(n, state)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pix = img.load()
    for mark, opt in marks.items():
        if mark in state:
            for row in range(height / 2 * opt['pos'][0], height / 2 * (opt['pos'][0]+1)):
                for col in range(width / 2 * opt['pos'][1], width / 2 * (opt['pos'][1]+1)):
                    pix[col, row] = opt['color']
    img.save('box%02d.png' % n)
