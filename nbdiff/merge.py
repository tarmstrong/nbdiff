from . import diff
from . import comparable
from .notebook_diff import (
    diff_result_to_cell,
)
import IPython.nbformat.current as nbformat
import itertools as it
import copy


def merge(local, base, remote, check_modified=False):
    """Generate unmerged series of changes (including conflicts).

    By diffing the two diffs, we find *changes* that are
    on the local branch, the remote branch, or both.
    We arbitrarily choose the "local" branch to be the "before"
    and the "remote" branch to be the "after" in the diff algorithm.

    Therefore:
    If a change is "deleted", that means that it occurs only on
    the local branch. If a change is "added" that means it occurs only on
    the remote branch. If a change is "unchanged", that means it occurs
    in both branches. Either the same addition or same deletion occurred in
    both branches, or the cell was not changed in either branch.

    Parameters
    ----------
    local : list
        A sequence representing the items on the local branch.
    base : dict
        A sequence representing the items on the base branch
    remote : dict
        A sequence representing the items on the remote branch.

    Returns
    -------
    result : A diff result comparing the changes on the local and remote
             branches.
    """
    base_local = diff.diff(base, local, check_modified=check_modified)
    base_remote = diff.diff(base, remote, check_modified=check_modified)
    merge = diff.diff(base_local, base_remote)
    return merge


def notebook_merge(local, base, remote, check_modified=False):
    """Unify three notebooks into a single notebook with merge metadata.

    The result of this function is a valid notebook that can be loaded
    by the IPython Notebook front-end. This function adds additional
    cell metadata that the front-end Javascript uses to render the merge.

    Parameters
    ----------
    local : dict
        The local branch's version of the notebook.
    base : dict
        The last common ancestor of local and remote.
    remote : dict
        The remote branch's version of the notebook.

    Returns
    -------
    nb : A valid notebook containing merge metadata.
    """

    local_cells = get_cells(local)
    base_cells = get_cells(base)
    remote_cells = get_cells(remote)

    rows = []
    current_row = []
    empty_cell = lambda: {
        'cell_type': 'code',
        'language': 'python',
        'outputs': [],
        'prompt_number': 1,
        'text': ['Placeholder'],
        'metadata': {'state': 'empty'}
    }

    diff_of_diffs = merge(local_cells, base_cells, remote_cells)

    # For each item in the higher-order diff, create a "row" that
    # corresponds to a row in the NBDiff interface. A row contains:
    # | LOCAL | BASE | REMOTE |

    for item in diff_of_diffs:
        state = item['state']
        cell = copy.deepcopy(diff_result_to_cell(item['value']))
        if state == 'deleted':
            # This change is between base and local branches.
            # It can be an addition or a deletion.
            if cell['metadata']['state'] == 'unchanged':
                # This side doesn't have the change; wait
                # until we encounter the change to create the row.
                continue
            cell['metadata']['side'] = 'local'
            remote_cell = empty_cell()
            remote_cell['metadata']['side'] = 'remote'
            if cell['metadata']['state'] == 'deleted' \
                    or cell['metadata']['state'] == 'unchanged':
                base_cell = copy.deepcopy(cell)
            else:
                base_cell = empty_cell()
            base_cell['metadata']['side'] = 'base'
            # This change is on the right.
            current_row = [
                cell,
                base_cell,
                remote_cell,
            ]
        elif state == 'added':
            # This change is between base and remote branches.
            # It can be an addition or a deletion.
            cell['metadata']['side'] = 'remote'
            if cell['metadata']['state'] == 'unchanged':
                # This side doesn't have the change; wait
                # until we encounter the change to create the row.
                continue
            if cell['metadata']['state'] == 'deleted':
                base_cell = copy.deepcopy(cell)
                base_cell['metadata']['state'] = 'unchanged'
                local_cell = copy.deepcopy(cell)
                local_cell['metadata']['state'] = 'unchanged'
            else:
                base_cell = empty_cell()
                local_cell = empty_cell()
            base_cell['metadata']['side'] = 'base'
            local_cell['metadata']['side'] = 'local'
            current_row = [
                local_cell,
                base_cell,
                cell,
            ]
        elif state == 'unchanged':
            # The same item occurs between base-local and base-remote.
            # This happens if both branches made the same change, whether
            # that is an addition or deletion. If neither branches
            # changed a given cell, that cell shows up here too.
            cell1 = copy.deepcopy(cell)
            cell3 = copy.deepcopy(cell)
            if cell['metadata']['state'] == 'deleted' \
                    or cell['metadata']['state'] == 'unchanged':
                # If the change is a deletion, the cell-to-be-deleted
                # should in the base as 'unchanged'. The user will
                # choose to make it deleted.
                cell2 = copy.deepcopy(cell)
                cell2['metadata']['state'] = 'unchanged'
            else:
                # If the change is an addition, it should not
                # show in the base; the user must add it to the merged version.
                cell2 = empty_cell()
            cell1['metadata']['side'] = 'local'
            cell2['metadata']['side'] = 'base'
            cell3['metadata']['side'] = 'remote'
            current_row = [
                cell1,
                cell2,
                cell3,
            ]

        rows.append(current_row)

    # Chain all rows together; create a flat array from the nested array.
    # Use the base notebook's notebook-level metadata (title, version, etc.)

    result_notebook = local
    if len(result_notebook['worksheets']) == 0:
        result_notebook['worksheets'] = [nbformat.new_worksheet()]

    new_cell_array = list(it.chain.from_iterable(rows))
    result_notebook['worksheets'][0]['cells'] = new_cell_array

    result_notebook['metadata']['nbdiff-type'] = 'merge'

    return result_notebook


def get_cells(notebook, check_modified=False):
    try:
        cells = [
            comparable.CellComparator(cell, check_modified=check_modified)
            for cell in
            notebook['worksheets'][0]['cells']
        ]
    except IndexError:
        cells = []
    except KeyError:
        cells = []
    return cells
