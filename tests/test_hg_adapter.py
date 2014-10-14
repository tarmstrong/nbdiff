import hglib
import os

from nbdiff.adapter import hg_adapter as hg
from testfixtures import tempdir, compare


@tempdir()
def test_get_modified_notebooks_empty(d):
    d.makedir('output')
    os.chdir(os.path.join(d.path, 'output'))
    hglib.init()
    adapter = hg.HgAdapter()
    result = adapter.get_modified_notebooks()
    assert result == []


@tempdir()
def test_get_modified_notebooks(d):
    os.chdir(d.path)
    client = hglib.init()
    client.open()
    d.makedir('first')
    d.makedir('first/second')
    path = d.write('first/second/1.ipynb', 'initial')
    compare(d.read('first/second/1.ipynb'), 'initial')
    client.add('first/second/1.ipynb')
    client.commit("message")
    file = open(path, 'w')
    file.write("modified")
    file.close()
    compare(d.read('first/second/1.ipynb'), 'modified')
    os.chdir(os.path.join(d.path, 'first'))

    adapter = hg.HgAdapter()
    result = adapter.get_modified_notebooks()
    assert len(result) == 1
    compare(result[0][0].read(), 'modified')
    compare(result[0][1].read(), 'initial')
    compare(result[0][2], 'first/second/1.ipynb')


@tempdir()
def test_get_unmerged_notebooks_empty(d):
    d.makedir('output')
    os.chdir(os.path.join(d.path, 'output'))
    hglib.init()
    adapter = hg.HgAdapter()
    result = adapter.get_unmerged_notebooks()
    assert result == []
