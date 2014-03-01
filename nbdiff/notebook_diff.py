from .diff import diff_modified_items
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
    cell_list.append({
        'cell_type': 'heading',
        'level': 1,
        'source': 'potato',
        'metadata': {
            'state': 'modified',
            'header-diff': [
                {'state': 'added', 'value': 'isAdded adsf'},
                {'state': 'deleted', 'value': 'isDeleted'},
                {'state': 'unchanged', 'value': 'isUnchanged'},
            ]
        }
    })
    cell_list.append({
        'cell_type': 'heading',
        'level': 1,
        'source': 'potato',
        'metadata': {
            'state': 'unchanged',
        }
    })

    nb1['worksheets'][0]['cells'] = cell_list
    nb1['metadata']['nbdiff-type'] = 'diff'

    return nb1
