from .merge import cells_diff, diff_result_to_cell


def notebook_diff(nb1, nb2):

    nb1_cells = nb1['worksheets'][0]['cells']
    nb2_cells = nb2['worksheets'][0]['cells']

    diffed_nb = cells_diff(nb1_cells, nb2_cells)

    cell_list = list()
    for item in diffed_nb:
        cell = diff_result_to_cell(item)
        cell_list.append(cell)

    nb1['worksheets'][0]['cells'] = cell_list
    nb1['metadata']['ndiff-type'] = 'diff'

    return nb1
