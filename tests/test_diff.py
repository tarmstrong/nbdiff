from nose.tools import eq_

from nbdiff.diff import (
    lcs_dynamic,
    lcs,
)


def test_lcs():
    a = ['x', 'y', 'z', 'a', 'b', 'c']
    b = ['a', 'b', 'c', 'd']
    result = lcs_dynamic(a, b)
    eq_(result, 3)
    result = lcs(a, b)
    eq_(result, 3)

