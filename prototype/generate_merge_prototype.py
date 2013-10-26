'''You probably don't want to run this script.'''
from mako.template import Template
import re
import BeautifulSoup as b

first_cells = []
for i in range(15):
    with open('merge-cells/cell-1-{i:d}.html'.format(i=i)) as f:
        cell_content = f.read()
        if len(cell_content) > 0:
            first_cells.append(cell_content)

second_cells = []
for i in range(15):
    with open('merge-cells/cell-2-{i:d}.html'.format(i=i)) as f:
        cell_content = re.sub(r'<div', '\n<div', f.read())
        cell_content = re.sub(r'</div', '\n</div', cell_content)
        if len(cell_content) > 0:
            second_cells.append(cell_content)

third_cells = []
for i in range(15):
    with open('merge-cells/cell-3-{i:d}.html'.format(i=i)) as f:
        cell_content = re.sub(r'<div', '\n<div', f.read())
        cell_content = re.sub(r'</div', '\n</div', cell_content)
        if len(cell_content) > 0:
            third_cells.append(cell_content)

zcells = zip(first_cells, second_cells, third_cells)


# TODO Use arrow symbols instead of "right" and "left"
rowfmt = '''
<!-- ROW #{idx:d} -->

<div class='row'>

<!-- ROW #{idx:d} : Left (local) pane -->
<div class='row-cell-merge-local'>{local}</div>

<!-- ROW #{idx:d} : Thin control pane between local and base -->
<div class='row-cell-merge-controls-local'>
<input type='button' value='right' data-cell-idx='{idx:d}' class='merge-arrow-right' />
</div>

<!-- This is confusing: the right-hand-side comes before the middle.
I couldn't get it to work otherwise.
-->
<!-- ROW #{idx:d} : Right (remote) pane -->
<div class='row-cell-merge-remote'>{remote}</div>

<!-- ROW #{idx:d} : Thin control pane between base and remote -->
<div class='row-cell-merge-controls-remote'>
<input type='button' value='left' data-cell-idx='{idx:d}' class='merge-arrow-left' />
</div>

<!-- ROW #{idx:d} : Middle (base) pane -->
<div class='row-cell-merge-base'>{base}</div>
</div>

<!-- END OF ROW #{idx:d} -->

'''

rendered_cells = "\n".join([rowfmt.format(local=a, base=b, remote=c, idx=i) for i, (a, b, c) in enumerate(zcells)])

rendered_full = Template(open('nbdiff-template.html').read()).render(cells=rendered_cells)

open('merge.html', 'w').write(rendered_full)


