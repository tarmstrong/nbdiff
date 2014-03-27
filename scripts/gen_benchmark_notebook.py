# generate two notebook files that are large enough for benchmarking.

import IPython.nbformat.current as nbformat
import random


def new_code_cell():
    nlines = random.randint(0, 30)
    input = [
        str(random.random())
        for i in range(nlines)
    ]
    code_cell = nbformat.new_code_cell(input=input)
    return code_cell


cells = [
    new_code_cell()
    for i in range(100)
]

worksheet = nbformat.new_worksheet(cells=cells)

nb = nbformat.new_notebook(name='Test Notebook')

nb['worksheets'].append(worksheet)

with open('nb1.ipynb', 'w') as out:
    nbformat.write(nb, out, 'ipynb')


cells = nb['worksheets'][0]['cells']


# Take original notebook and make changes to it
ncells = len(cells)
to_change = [random.choice(list(range(ncells))) for i in range(10)]
for tc in to_change:
    input = cells[tc]['input']
    ninput = len(input)
    to_delete = [random.choice(list(range(ninput))) for i in range(10)]
    for td in to_delete:
        if td < len(input):
            del input[td]
    cells[tc]['input'] = input

ncells = len(cells)
removed = [random.choice(list(range(ncells))) for i in range(10)]
for r in removed:
    if r < len(cells):
        del cells[r]

nb['worksheets'][0]['cells'] = cells


with open('nb2.ipynb', 'w') as out:
    nbformat.write(nb, out, 'ipynb')


