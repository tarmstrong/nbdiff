__author__ = 'Lina'

import itertools as it
import collections


def diff(before, after):
    grid = create_grid(before, after)
    dps = diff_points(grid)
    result = []
    for kind, col, row in dps:
        if kind == 'unchanged':
            value = before[col]
        elif kind == 'deleted':
            value = before[col]
        elif kind == 'added':
            value = after[row]
        result.append({
            'state': kind,
            'value': value,
        })
    return result


def diff_points(grid):
    # cols = before; rows = after
    ncols = len(grid)
    nrows = len(grid[0])
    colvals = list(range(ncols))
    rowvals = list(range(nrows))

    lcs_result = lcs(grid)
    matched_cols = [r[0] for r in lcs_result]
    matched_rows = [r[1] for r in lcs_result]

    cur_col = 0
    cur_row = 0

    result = []
    while cur_col < ncols or cur_row < nrows:
        passfirst = cur_col < ncols and cur_row < nrows
        goodcol = cur_col < ncols
        goodrow = cur_row < nrows
        if passfirst and (cur_col, cur_row) == lcs_result[0]:
            lcs_result.pop(0)
            matched_cols.pop(0)
            matched_rows.pop(0)
            result.append(('unchanged', cur_col, cur_row))
            cur_col += 1
            cur_row += 1
        elif goodcol and (not matched_cols or cur_col != matched_cols[0]):
            result.append(('deleted', cur_col, None))
            cur_col += 1
        elif goodrow and (not matched_rows or cur_row != matched_rows[0]):
            result.append(('added', None, cur_row))
            cur_row += 1

    return result


def create_grid(before, after):
    blen = len(before)
    alen = len(after)
    all_comps = [b == a for b, a in it.product(before, after)]
    return [all_comps[i*(blen-1):i*(blen-1)+blen-1] for i in range(len(before))]


def find_matches(col, colNum):
    result = []
    for j in range(len(col)):
        if col[j]:
            result.append((colNum, j))
    return result


def lcs(grid):
    kcs = find_candidates(grid)
    highest = max(kcs.keys())
    last_point = kcs[highest][-1]
    cur = highest - 1
    acc = [last_point]
    while cur > 0:
        comp = acc[-1]
        cx, cy = comp
        acc.append([(x, y) for (x, y) in reversed(kcs[cur]) if cx > x and cy > y][-1])
        cur -= 1

    return list(reversed(acc))


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
