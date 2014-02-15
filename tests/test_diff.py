from nose.tools import eq_
import itertools as it
import collections
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
    count_similar_lines,
    check_modified,
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

def test_count_similar_lines():
    A = {u'input':[u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    B = {u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}
    result = count_similar_lines(A, B)

    expected = 2
    eq_(result, expected)

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

def test_check_modified():
    A = {u'input':[u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    B = {u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}

    result = check_modified(A, B)
    expected = True
    eq_(result, expected)

def test_diff_points():
    A = [{u'input':[u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}]
    B = [{u'input':[u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}]

    result = diff_points(A, B)

    expected = [
        ('modified', 0, None),
        ('modified', None, 0),
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