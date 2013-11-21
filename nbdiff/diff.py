__author__ = 'Lina'

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
            x = x
            if x == oldx:
                continue
            d[x].append((i,j))
    return dict(d)


def check_match(point, k):
    result = []
    k_keys = k.keys()
    max_k = max(k_keys)
    new_max_k = max_k + 1
    k_range = k_keys + [new_max_k]
    for x in k_range:
        if x == 1:
            continue
        if point[1] < x-2:
            continue
        first_elts = [max([l[0] for l in k[x-1]])]
        second_elts = [min([l[1] for l in k[x-1]])]
        for d in range(len(second_elts)):
            if point[0] > first_elts[d] and point[1] < second_elts[d]:
                result.append(x-1)
                break

    first_elts = [l[0] for l in k[new_max_k-1]]
    second_elts = [l[1] for l in k[new_max_k-1]]
    for d in range(len(second_elts)):
        if point[0] > first_elts[d] and point[1] > second_elts[d]:
            result.append(new_max_k)
            break
    if len(result) > 0:
        actual_result = result[0]
        assert point[1] >= actual_result-1
        return (result)[0]
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
