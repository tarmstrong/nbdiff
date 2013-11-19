__author__ = 'Lina'

# nosetests DiffingFunctions.py

from nose.tools import eq_
import itertools as it
import collections

def find_matches(col, colNum):
    result = []
    for j in range(len(col)):
        if col[j]:
            result.append((colNum, j))
    return result

def process_col(k, col, colNum):
    matches = find_matches(col, colNum)
    d = collections.defaultdict(lambda:[])
    x = 0
    for (i, j) in matches:
        oldx = x
        if not k and not d[1]:
            d[1].append((i,j))
        elif k:
            x = check_match((i,j),k)
            if x is None:
                continue
            #for x in xs:
            x = x
            if x == oldx:
                continue
            d[x].append((i,j))
    return dict(d)

def check_match(point, k):
    result = []
    for x in k.keys():
        first_elts = [l[0] for l in k[x]]
        second_elts = [l[1] for l in k[x]]
        for d in range(len(second_elts)):
            if point[0] > first_elts[d] and point[1] > second_elts[d]:
                result.append(x + 1)
                break
            if point[0] > first_elts[d] and point[1] < second_elts[d]:
                result.append(x)
                break
    if len(result) > 0:
        return max(result)
    else:
        return None

def add_results(k, result):
    finalResult = collections.defaultdict(lambda:[],k)
    for x in result.keys():
        finalResult[x] = finalResult[x] + result[x]
    return finalResult

def find_candidates(grid):
    k = collections.defaultdict(lambda:[])
    for colNum in range(len(grid)):
        k = add_results(k,process_col(k, grid[colNum], colNum))
    return dict(k)

# tests

def test_find_candidates():
    A = "abcabba"
    B = "cbabac"
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
    expected = {1:[(0,2),(1,1),(2,0)],
                2:[(1,3),(3,2),(4,1)],
                3:[(2,5),(3,4),(4,3),(6,2)],
                4:[(6,4)]}
    eq_(result, expected)


def test_add_results():
    k = {1:[(0,2)]}
    newk = {1:[(1,1)],2:[(1,3)]}
    result = add_results(k, newk)
    expected = {1:[(0,2),(1,1)],2:[(1,3)]}
    eq_(result, expected)

def test_find_matches():
    A = "abcabba"
    B = "cbabac"
    grid = [[a == b for (a, b) in list(it.product(A, B))][i * len(B):i * len(B) + len(B)] for i in range(len(A))]
    k = [[(len(A), len(B))] for x in range(min(len(A), len(B)) + 1)]
    colNum = 0
    result = find_matches(grid[colNum], colNum)
    expected = [(0, 2),(0,4)]
    eq_(result, expected)

def test_process_col():
    d = {1:[(0, 2)]}
    a = [False, True, False, True, False, False]
    col = 1
    expected = {1:[(1,1)], 2:[(1,3)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {}
    a = [False, True, False, True, False, False]
    col = 1
    expected = {1:[(1,1)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1:[(0,2)]}
    a = [False, True, False, True, False, True]
    col = 1
    expected = {1:[(1,1)], 2:[(1,3)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1:[(0,2),(1,1),(2,0)], 2:[(1,3)],3:[(2,5)]}
    a = [False, False, False, False, True, False]
    col = 3
    expected = {3:[(3,4)]}
    result = process_col(d, a, col)
    eq_(result, expected)

def test_check_match():
    point = (1,3)
    k = {1:[(0,2)]}
    expected = 2
    result = check_match(point, k)
    eq_(result, expected)

    point = (1,1)
    k = {1:[(0,2)]}
    expected = 1
    result = check_match(point, k)
    eq_(result, expected)

    point = (1,2)
    k = {1:[(0,2)]}
    expected = None
    result = check_match(point, k)
    eq_(result, expected)

    point = (3,4)
    k = {1:[(0,2),(1,1),(2,0)], 2:[(1,3)],3:[(2,5)]}
    expected = 3
    result = check_match(point, k)
    eq_(result, expected)

    point = (2, 0)
    k = {1:[(0,2),(1,1)], 2:[(1,3)]}
    expected = 1
    result = check_match(point, k)
    eq_(result, expected)