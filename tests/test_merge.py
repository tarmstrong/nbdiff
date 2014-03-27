import IPython.nbformat.current as nbformat

from nbdiff.merge import (
    notebook_merge,
    merge,
)


# Regression test for bug #196
def test_empty_notebook():
    notebook = nbformat.new_notebook()
    notebook2 = nbformat.new_notebook()
    notebook3 = nbformat.new_notebook()
    result = notebook_merge(notebook, notebook2, notebook3)
    assert result['metadata']['nbdiff-type'] == 'merge'


def test_basic_notebook_merge():
    notebook = nbformat.new_notebook()
    code_cell = nbformat.new_code_cell(input=['a', 'b'])
    notebook['worksheets'] = [
        {'cells': [code_cell]}
    ]
    notebook2 = nbformat.new_notebook()
    notebook3 = nbformat.new_notebook()
    code_cell = nbformat.new_code_cell(input=['a', 'b'])
    notebook3['worksheets'] = [
        {'cells': [code_cell]}
    ]
    result = notebook_merge(notebook, notebook2, notebook3)
    result_cells = result['worksheets'][0]['cells']
    state = result_cells[0]['metadata']['state']
    assert state == 'added'


def test_basic_merge():
    lines_local = ['a', 'b', 'c']
    lines_base = ['a', 'b']
    lines_remote = ['a', 'b', 'c']
    result = merge(lines_local, lines_base, lines_remote)
    assert result[0]['state'] == 'unchanged'
    assert result[0]['value']['state'] == 'unchanged'
