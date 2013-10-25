'''You probably don't want to run this script.'''
from mako.template import Template
import re
import BeautifulSoup as b

first_cells = []
for i in range(15):
    with open('cells/cell-1-{i:d}.html'.format(i=i)) as f:
        cell_content = f.read()
        if len(cell_content) > 0:
            first_cells.append(cell_content)

second_cells = []
for i in range(15):
    with open('cells/cell-2-{i:d}.html'.format(i=i)) as f:
        cell_content = f.read()
        if len(cell_content) > 0:
            second_cells.append(cell_content)

zcells = zip(first_cells, second_cells)

# for some reason the middle cell has to be at the bottom? whyyy?
rowfmt = '''
<div class='row'>
<div class='row-cell-diff-left'>{}</div>
<div class='row-cell-diff-right'>{}</div>
<div class='row-cell-diff-middle'>
<input type='checkbox' data-cell-idx='{idx:d}' class='staging-checkbox' checked />
</div>
</div>'''

rendered_cells = "\n".join([rowfmt.format(a, b, idx=i) for i, (a, b) in enumerate(zcells)])

rendered_full = Template(open('nbdiff-template.html').read()).render(cells=rendered_cells)

open('diff.html', 'w').write(rendered_full)

