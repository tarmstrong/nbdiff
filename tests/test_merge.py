import IPython.nbformat.current as nbformat
from nose.tools import eq_

from nbdiff.merge import (
    notebook_merge,
)


# Regression test for bug #196
def test_empty_notebook():
    notebook = nbformat.new_notebook()
    notebook2 = nbformat.new_notebook()
    notebook3 = nbformat.new_notebook()
    notebook_merge(notebook, notebook2, notebook3)
