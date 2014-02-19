from nose.tools import eq_
import itertools as it
import collections
import nbdiff
import nbdiff.diff as d
import nbdiff.comparable as c
from nbdiff.diff import (
    add_results,
    find_candidates,
    find_matches,
    process_col,
    check_match,
    lcs,
    diff_points,
    create_grid,
    diff,
)

def test_diff():
    A = [{u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},{u'input':[u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}]
    B = [{u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}]
    result = diff(A, B)
    expected = [
        {"state": 'unchanged', 'value': {u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}},
        {"state": 'deleted', 'value': {u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}}
    ]
    eq_(result, expected)
    #diff("aaaaaaaaaaaaaaaaaaaa", "bbbbbbaaaaaaaaaaabbbbbbbbbbb")
    #diff("cabcdef", "abdef")
    #diff("ca", "abdef")
'''
def test_count_similar_lines():
    A = {u'input':[u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    B = {u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}
    result = count_similar_lines(A, B)

    expected = 2
    eq_(result, expected)
'''
def test_create_grid():
    A = "abcabba"
    B = "cbabac"
    expected = [
        # c      b     a     b      a      c
        [False, False, True, False, True, False],  # a
        [False, True, False, True, False, False],  # b
        [True, False, False, False, False, True],  # c
        [False, False, True, False, True, False],  # a
        [False, True, False, True, False, False],  # b
        [False, True, False, True, False, False],  # b
        [False, False, True, False, True, False]   # a
    ]
    grid = create_grid(A, B)
    eq_(grid, expected)

    A, B = ("cabcdef", "abdef")
    grid = create_grid(A, B)
    assert len([True for col in grid if len(col) == 0]) == 0
'''
def test_check_modified():
    A = {u'input':[u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    B = {u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}

    result = check_modified(A, B)
    expected = True
    eq_(result, expected)
'''
def test_diff_points():
    A = [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']
    B = [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']

    grid = create_grid(A,B)

    result = diff_points(grid)

    expected = [
        ('deleted', 0, None),
        ('added', None, 0),
        ('unchanged', 1, 1),
        ('unchanged', 2, 2),
        ('deleted', 3, None),
        ('added', None, 3),
    ]
    eq_(result, expected)


def test_find_candidates():
    grid = [
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [True, False, False, False, False, True],
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [False, True, False, True, False, False],
        [False, False, True, False, True, False]
    ]
    result = find_candidates(grid)
    expected = {
        1: [(0, 2), (1, 1), (2, 0)],
        2: [(1, 3), (3, 2), (4, 1)],
        3: [(2, 5), (3, 4), (4, 3), (6, 2)],
        4: [(6, 4)],
    }
    eq_(result, expected)

    grid = [
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True]
    ]
    result = find_candidates(grid)
    expected = {1: [(0, 1)], 2: [(1, 2)]}
    eq_(result, expected)


def test_lcs():
    grid = [
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [True, False, False, False, False, True],
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [False, True, False, True, False, False],
        [False, False, True, False, True, False]
    ]
    result = lcs(grid)
    expected = [(1, 1), (3, 2), (4, 3), (6, 4)]
    eq_(result, expected)

    grid = [
        [False, False, True, False, True, False],
        [False, False, False, True, False, False],
        [True, False, False, False, False, True],
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [False, True, False, True, False, False],
        [False, False, True, False, True, False]
    ]
    result = lcs(grid)
    expected = [(2, 0), (3, 2), (4, 3), (6, 4)]
    eq_(result, expected)

    grid = [
        [True, True, True, True, True, True],
        [True, True, True, True, True, True],
        [True, True, True, True, True, True],
        [True, True, True, True, True, True],
        [True, True, True, True, True, True],
        [True, True, True, True, True, True],
        [True, True, True, True, True, True]
    ]
    result = lcs(grid)
    expected = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    eq_(result, expected)

    grid = [
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True],
        [False, True, True]
    ]
    result = lcs(grid)
    expected = [(0, 1), (1, 2)]
    eq_(result, expected)


def test_lcs_noequals():
    # See issue #128
    grid = [[False, False], [False, False]]
    result = lcs(grid)
    eq_(result, [])


def test_add_results():
    k = {1: [(0, 2)]}
    newk = {1: [(1, 1)], 2: [(1, 3)]}
    result = add_results(k, newk)
    expected = {1: [(0, 2), (1, 1)], 2: [(1, 3)]}
    eq_(result, expected)


def test_find_matches():
    A = "abcabba"
    B = "cbabac"
    prod = list(it.product(A, B))
    grid = [
        [
            a == b
            for (a, b) in
            prod
        ][i * len(B):i * len(B) + len(B)]
        for i in range(len(A))
    ]
    colNum = 0
    result = find_matches(grid[colNum], colNum)
    expected = [(0, 2), (0, 4)]
    eq_(result, expected)


def test_process_col():
    d = {1: [(0, 2)]}
    a = [False, True, False, True, False, False]
    col = 1
    expected = {1: [(1, 1)], 2: [(1, 3)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {}
    a = [False, True, False, True, False, False]
    col = 1
    expected = {1: [(1, 1)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1: [(0, 2)]}
    a = [False, True, False, True, False, True]
    col = 1
    expected = {1: [(1, 1)], 2: [(1, 3)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1: [(0, 2), (1, 1), (2, 0)], 2: [(1, 3)], 3: [(2, 5)]}
    a = [False, False, False, False, True, False]
    col = 3
    expected = {3: [(3, 4)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    grid = [
        [False, True, True],
        [False, True, True],
        [False, True, True],
    ]
    d = {1: [(0, 1)]}
    a = grid[1]
    col = 1
    expected = {2: [(1, 2)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1: [(0, 1)], 2: [(1, 2)]}
    a = grid[2]
    col = 2
    expected = {}
    result = process_col(d, a, col)
    eq_(result, expected)


def test_check_match():
    point = (1, 3)
    k = {1: [(0, 2)]}
    expected = 2
    result = check_match(point, k)
    eq_(result, expected)

    point = (1, 1)
    k = {1: [(0, 2)]}
    expected = 1
    result = check_match(point, k)
    eq_(result, expected)

    point = (1, 2)
    k = {1: [(0, 2)]}
    expected = None
    result = check_match(point, k)
    eq_(result, expected)

    point = (3, 4)
    k = {1: [(0, 2), (1, 1), (2, 0)], 2: [(1, 3)], 3: [(2, 5)]}
    expected = 3
    result = check_match(point, k)
    eq_(result, expected)

    point = (2, 0)
    k = {1: [(0, 2), (1, 1)], 2: [(1, 3)]}
    expected = 1
    result = check_match(point, k)
    eq_(result, expected)

    point = (5, 1)
    k = {
        1: [(0, 2), (1, 1), (2, 0)],
        2: [(1, 3), (3, 2), (4, 1)],
        3: [(2, 5), (3, 4), (4, 3)]
    }
    expected = None
    result = check_match(point, k)
    eq_(result, expected)

    #print 'boop boop'
    point = (2, 1)
    k = {1: [(0, 1)], 2: [(1, 2)]}
    expected = None
    result = check_match(point, k)
    eq_(result, expected)


# some test data

cell1 = {
     "cell_type": "code",
     "collapsed": False,
     "input": [
         "x",
         "x",
         "x",
         "x",
         "x",
         "x",
         "y"
     ],
     "language": "python",
     "metadata": {
      "slideshow": {
       "slide_type": "fragment"
      }
     },
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Hello, world!\n",
        "Hello, world!\n"
       ]
      }
     ],
     "prompt_number": 29
    }


cell2 =    {
     "cell_type": "code",
     "collapsed": False,
     "input": [
         "x",
         "x",
         "x",
         "x",
         "x",
         "x"
     ],
     "language": "python",
     "metadata": {
      "slideshow": {
       "slide_type": "fragment"
      }
     },
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Hello, world!\n",
        "Hello, world!\n"
       ]
      }
     ],
     "prompt_number": 29
    }



class FakeComparator(object):
    '''Test comparator object. Will compare as modified if it is "close to"
    the specified values'''
    def __init__(self, foo, closeto=[]):
        self.foo = foo
        self.closeto = closeto

    def __eq__(self, other):
        if other.foo in self.closeto:
            return c.BooleanPlus(True, True)
        else:
            return self.foo == other.foo

def test_modified_false():
    # this still works...
    result = d.diff(['a', 'b', 'c'], ['b', 'c'], check_modified=False)
    expected =  expected = [
        {"state": 'deleted', 'value': 'a'},
        {"state": 'unchanged', 'value': 'b'},
        {"state": 'unchanged', 'value': 'c'},
    ]
    eq_(result, expected)


def test_modified_true():
    # it doesn't break strings when check_modified is True
    result =  d.diff(['a', 'b', 'c'], ['b', 'c'], check_modified=True)
    expected = [
        {"state": 'deleted', 'value': 'a'},
        {"state": 'unchanged', 'value': 'b'},
        {"state": 'unchanged', 'value': 'c'},
    ]
    eq_(result, expected)


def test_cell_comparator():
    # CellComparators do actually produce booleanpluses if they are similar enough

    c1 = c.CellComparator(cell1)
    c2 = c.CellComparator(cell2)

  #  assert type(c1 == c2) == c.BooleanPlus

    result = d.diff([c1, c2, c2, c2], [c2, c2, c2, c2], check_modified=True)
    print result
   # assert result[0]['state'] == 'modified'

    assert result[0]['state'] == 'modified'
    assert result[1]['state'] == 'unchanged'
    assert result[2]['state'] == 'unchanged'
    assert result[3]['state'] == 'unchanged'

 

def test_cell_fakeComparator():
    c1 = FakeComparator(1, [2, 3])
    c2 = FakeComparator(2, [1, 3])
    c3 = FakeComparator(10, [])

    c4 = FakeComparator(2, [])
    c5 = FakeComparator(3, [])

    # c1 -> c4
    # c2 -> c5
    # c3 -> deleted
    result = d.diff([c1, c2, c3], [c4, c5], check_modified=True)
    expected = [
        {"state": 'modified', 'originalvalue': '1, [2, 3]', 'modifiedvalue': '2, []'},
        {"state": 'modified', 'originalvalue': '2, [1, 3]', 'modifiedvalue': '3, []'},
        {"state": 'deleted', 'value': '10, []'},
    ]

    assert result[0]['state'] == 'modified'
    assert result[1]['state'] == 'modified'
    assert result[2]['state'] == 'deleted'
