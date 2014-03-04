from .diff import diff
from .comparable import CellComparator, LineComparator


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


def diff_modified_items(cellslist):
    result = {}
    for i in range(len(cellslist)):
        if cellslist[i]['state'] == 'modified':
            if cellslist[i]['originalvalue'].data['cell_type'] == 'heading':
                result[i] = diff(
                    cellslist[i]['originalvalue'].data["source"].split(),
                    cellslist[i]['modifiedvalue'].data["source"].split(),
                )
            else:
                result[i] = diff(
                    cellslist[i]['originalvalue'].data["input"].splitlines(),
                    cellslist[i]['modifiedvalue'].data["input"].splitlines(),
                )
    return result


def diff_result_to_cell(item):
    '''diff.diff returns a dictionary with all the information we need,
    but we want to extract the cell and change its metadata.'''
    state = item['state']
    if state == 'modified':
        new_cell = item['modifiedvalue'].data
        old_cell = item['originalvalue'].data
        new_cell['metadata']['state'] = state
        new_cell['metadata']['original'] = old_cell
        cell = new_cell
    else:
        cell = item['value'].data
        cell['metadata']['state'] = state
    return cell


def cells_diff(before_cells, after_cells, check_modified=False):
    '''Diff two arrays of cells.'''
    before_comps = [
        CellComparator(cell, check_modified=check_modified)
        for cell in before_cells
    ]
    after_comps = [
        CellComparator(cell, check_modified=check_modified)
        for cell in after_cells
    ]
    diff_result = diff(
        before_comps,
        after_comps,
        check_modified=check_modified
    )
    return diff_result


def words_diff(before_words, after_words):
    '''Diff the words in two strings.

    This is intended for use in diffing prose and other forms of text
    where line breaks have little semantic value.

    Parameters
    ----------
    before_words : str
        A string to be used as the baseline version.
    after_words : str
        A string to be compared against the baseline.

    Returns
    -------
    diff_result : A list of dictionaries containing diff information.
    '''
    before_comps = before_words.split()
    after_comps = after_words.split()

    diff_result = diff(
        before_comps,
        after_comps
    )
    return diff_result


def lines_diff(before_lines, after_lines, check_modified=False):
    '''Diff the lines in two strings.

    Parameters
    ----------
    before_lines : iterable
        Iterable containing lines used as the baseline version.
    after_lines : iterable
        Iterable containing lines to be compared against the baseline.

    Returns
    -------
    diff_result : A list of dictionaries containing diff information.
    '''
    before_comps = [
        LineComparator(line, check_modified=check_modified)
        for line in before_lines
    ]
    after_comps = [
        LineComparator(line, check_modified=check_modified)
        for line in after_lines
    ]
    diff_result = diff(
        before_comps,
        after_comps,
        check_modified=check_modified
    )
    return diff_result
