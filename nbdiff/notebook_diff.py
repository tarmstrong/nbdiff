from .diff import diff
from .merge import cells_diff, diff_result_to_cell


def notebook_diff(nb1, nb2, check_modified=True):

    nb1_cells = nb1['worksheets'][0]['cells']
    nb2_cells = nb2['worksheets'][0]['cells']

    diffed_nb = cells_diff(nb1_cells, nb2_cells, check_modified=check_modified)
    line_diffs = diff_modified_items(diffed_nb)

    cell_list = list()
    for i, item in enumerate(diffed_nb):
        cell = diff_result_to_cell(item)
        if i in line_diffs:
            cell['metadata']['line-diff'] = line_diffs[i]
        cell_list.append(cell)

    nb1['worksheets'][0]['cells'] = cell_list
    nb1['metadata']['nbdiff-type'] = 'diff'

    return nb1

def diff_modified_items(cellslist):
    result = {}
    for i in range(len(cellslist)):
        if cellslist[i]['state'] == 'modified':
            result[i] = diff(
                cellslist[i]['originalvalue'].data["input"].splitlines(),
                cellslist[i]['modifiedvalue'].data["input"].splitlines(),
            )
    return result