from nbdiff.adapter import git_adapter as g
from pretend import stub


def test_get_modified_notebooks_empty():
    g.subprocess = stub(check_output=lambda cmd: '')
    adapter = g.GitAdapter()
    result = adapter.get_modified_notebooks()
    assert result == []


def test_get_unmerged_notebooks_empty():
    g.subprocess = stub(check_output=lambda cmd: '')
    adapter = g.GitAdapter()
    result = adapter.get_unmerged_notebooks()
    assert result == []
