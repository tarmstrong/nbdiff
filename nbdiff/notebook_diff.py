from .diff import diff_modified_items
from .merge import cells_diff, diff_result_to_cell


def notebook_diff(nb1, nb2, check_modified=True):
    """Unify two notebooks into a single notebook with diff metadata.

    The result of this function is a valid notebook that can be loaded
    by the IPython Notebook front-end. This function adds additional
    cell metadata that the front-end Javascript uses to render the diffs.

    Parameters
    ----------
    nb1 : dict
        An IPython Notebook to use as the baseline version.
    nb2 : dict
        An IPython Notebook to compare against the baseline.
    check_modified : bool
        Whether or not to detect cell modification.

    Returns
    -------
    nb : A valid notebook containing diff metadata.
    """
    nb1_cells = nb1['worksheets'][0]['cells']
    nb2_cells = nb2['worksheets'][0]['cells']

    diffed_nb = cells_diff(nb1_cells, nb2_cells, check_modified=check_modified)
    line_diffs = diff_modified_items(diffed_nb)

    cell_list = list()
    for i, item in enumerate(diffed_nb):
        cell = diff_result_to_cell(item)
        if i in line_diffs:
            cell['metadata']['extra-diff-data'] = line_diffs[i]
        cell_list.append(cell)

    nb1['worksheets'][0]['cells'] = cell_list
    nb1['metadata']['nbdiff-type'] = 'diff'

    return nb1
