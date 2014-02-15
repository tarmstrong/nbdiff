
import itertools as it
import collections


def diff(before, after):
    grid = create_grid(before, after)
    nrows = len(grid[0])
    ncols = len(grid)
    dps = diff_points(before,after)
    #dps = diff_points(grid)
    result = []
    for kind, col, row in dps:
        if kind == 'unchanged':
            value = before[col]
            result.append({
                'state': kind,
                'value': value,
            })
        elif kind == 'deleted':
            assert col < ncols
            value = before[col]
            result.append({
                'state': kind,
                'value': value,
            })
        elif kind == 'added':
#            print
#            print dps
#            print 'row', row
#            print 'after', after
            assert row < nrows
            #if len(after) <= row:
            #    print grid
            value = after[row]
            result.append({
                'state': kind,
                'value': value,
            })
        elif kind == 'modified':
            assert col < ncols
            value = before[col]
            result.append({
                'state': kind,
                'value': value,
            })
            assert row < nrows
            value = after[row]
            result.append({
                'state': kind,
                'value': value,
            })
    return result


#def diff_points(grid):
def diff_points(before, after):
    # cols = before; rows = after
    grid = create_grid(before, after)
    ncols = len(grid)
    nrows = len(grid[0])

    lcs_result = lcs(grid)

#   print
#    print
    print 'lcs', lcs_result
    matched_cols = [r[0] for r in lcs_result]
    matched_rows = [r[1] for r in lcs_result]

    new_matched_cols = [r[0] for r in lcs_result]
    new_matched_rows = [r[1] for r in lcs_result]


    cur_col = 0
    cur_row = 0

    result = []
    while cur_col < ncols or cur_row < nrows:
        passfirst = cur_col < ncols and cur_row < nrows
        goodrow = cur_row < nrows
        goodcol = cur_col < ncols
        if passfirst and lcs_result and (cur_col, cur_row) == lcs_result[0]:
            lcs_result.pop(0)
            matched_cols.pop(0)
            matched_rows.pop(0)
            result.append(('unchanged', cur_col, cur_row))
            cur_col += 1
            cur_row += 1
        elif goodcol and (not matched_cols or cur_col != matched_cols[0]):
            modified = False
            assert cur_col < ncols
            for i in range(len(after)):
                if (i in new_matched_rows) == False:
                    print before
                    print after
                    if check_modified(before[cur_col], after[i]):
                        modified = True
                        result.append(('modified', cur_col, None))
                        break
            if modified == False:
                result.append(('deleted', cur_col, None))
            cur_col += 1
        elif goodrow and (not matched_rows or cur_row != matched_rows[0]):
            modified = False
            assert cur_row < nrows
            for j in range(len(before)):
                if (j in new_matched_cols) == False:
                    if check_modified(after[cur_row], before[j]):
                        modified = True
                        result.append(('modified', None, cur_row))
                        break
            if modified == False:
                result.append(('added', None, cur_row))
            cur_row += 1
#        print result

    return result

def count_similar_lines(cellA, cellB):
    grid = create_grid(cellA['input'], cellB['input'])
    #grid = create_grid(cellA, cellB)
    matches = []
    for colnum in range(len(grid)):
        new_matches = find_matches(grid[colnum],colnum)
        matches = matches + new_matches

    matched_cols = [r[0] for r in matches]
    matched_rows = [r[1] for r in matches]

    unique_cols = []
    [unique_cols.append(col) for col in matched_cols if col not in unique_cols]
    unique_rows = []
    [unique_rows.append(row) for row in matched_rows if row not in unique_rows]

    return min(len(unique_cols), len(unique_rows))

def check_modified(cellA, cellB):
    unchanged_count = count_similar_lines(cellA, cellB)
    similarity_percent = (2.0 * unchanged_count) / (len(cellA) + len(cellB))
    if similarity_percent >= 0.50:
        return True
    return False

def create_grid(before, after):
    ncols = len(before)
    nrows = len(after)
    all_comps = [b == a for b, a in it.product(before, after)]
    return [all_comps[col*(nrows):col*(nrows)+nrows] for col in range(ncols)]

def find_matches(col, colNum):
    result = []
    for j in range(len(col)):
        if col[j]:
            result.append((colNum, j))
    return result

def lcs(grid):
    acc = []
    kcs = find_candidates(grid)
    print grid
    if kcs:
        highest = max(kcs.keys())
        last_point = kcs[highest][-1]
        cur = highest - 1
        acc = [last_point]
        while cur > 0:
            comp = acc[-1]
            cx, cy = comp
            possibilities = [
                (x, y) for (x, y)
                in reversed(kcs[cur])
                if cx > x and cy > y
            ]
            if len(possibilities) > 0:
                acc.append(possibilities[-1])
            cur -= 1

    return list(reversed(acc))


def process_col(k, col, colNum):
    matches = find_matches(col, colNum)
    d = collections.defaultdict(lambda: [])
    x = 0
    for (i, j) in matches:
        oldx = x
        if not k and not d[1]:
            d[1].append((i, j))
        elif k:
            #print 'check_match', (i, j), k
            x = check_match((i, j), k)
            if x is None:
                continue
            x = x
            if x == oldx:
                continue
            d[x].append((i, j))
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
#        print
#        print 'K = ', x
        above_key = x - 1
        above_x = above_key == new_max_k and \
            10000 or max([l[0] for l in k[above_key]])
        above_y = above_key == new_max_k and \
            10000 or min([l[1] for l in k[above_key]])
        below_key = x - 2
        below_x = below_key < 1 and -1 or max([l[0] for l in k[below_key]])
        below_y = below_key < 1 and -1 or min([l[1] for l in k[below_key]])
        new_x, new_y = point
        if new_x > above_x and new_y < above_y and \
                new_x > below_x and new_y > below_y:
            result.append(x-1)

    below_key = new_max_k - 1
    below_x = below_key == 0 and -1 or max([l[0] for l in k[new_max_k-1]])
    below_y = below_key == 0 and -1 or min([l[1] for l in k[new_max_k-1]])
    new_x, new_y = point
    if new_x > below_x and new_y > below_y:
        result.append(new_max_k)
    if len(result) > 0:
        actual_result = result[0]
        #print result
        assert point[1] >= actual_result-1
        return (result)[0]
    else:
        return None


def add_results(k, result):
    finalResult = collections.defaultdict(lambda: [], k)
    for x in result.keys():
        finalResult[x] = finalResult[x] + result[x]
    return finalResult


def find_candidates(grid):
    k = collections.defaultdict(lambda: [])
    for colNum in range(len(grid)):
        k = add_results(k, process_col(k, grid[colNum], colNum))
    return dict(k)