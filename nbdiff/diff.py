__author__ = 'Lina'

# nosetests DiffingFunctions.py

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
