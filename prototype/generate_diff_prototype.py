'''You probably don't want to run this script.'''
from mako.template import Template
import re
import BeautifulSoup as b

first_cells = []
for i in range(15):
    with open('cells/cell-1-{i:d}.html'.format(i=i)) as f:
        first_cells.append(f.read())

second_cells = []
for i in range(15):
    with open('cells/cell-2-{i:d}.html'.format(i=i)) as f:
        second_cells.append(f.read())

zcells = zip(first_cells, second_cells)

rowfmt = "<div class='row'><div class='row-cell'>{}</div><div class='row-cell'>{}</div></div>"

rendered_cells = "\n".join([rowfmt.format(a, b) for a, b in zcells])

rendered_full = Template(open('nbdiff-template.html').read()).render(cells=rendered_cells)

open('diff.html', 'w').write(rendered_full)

