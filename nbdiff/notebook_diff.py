from .merge import cells_diff, diff_result_to_cell


def notebook_diff(nb1, nb2):

    nb1_cells = nb1['worksheets'][0]['cells']
    nb2_cells = nb2['worksheets'][0]['cells']

    diffed_nb = cells_diff(nb1_cells, nb2_cells)

    cell_list = list()
    for item in diffed_nb:
        cell = diff_result_to_cell(item)

        if item['state'] == 'added':
            cell['metadata']['side'] = 'local'
        elif item['state'] == 'deleted':
            cell['metadata']['side'] = 'remote'
        elif item['state'] == 'unchanged':
            cell['metadata']['side'] = 'local'

        # TODO we should also handle state = 'modified'

        cell_list.append(cell)

    nb1['worksheets'][0]['cells'] = cell_list
    nb1['metadata']['nbdiff-type'] = 'diff'

    return nb1
