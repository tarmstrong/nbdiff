from . import diff
from .comparable import CellComparator
import itertools as it
import copy


def notebook_merge(local, base, remote):
    '''Accept three parsed notebooks and create a new notebook
    with metadata added to say which branch it belongs to.'''
    local_cells = local['worksheets'][0]['cells']
    base_cells = base['worksheets'][0]['cells']
    remote_cells = remote['worksheets'][0]['cells']
    local_diff = cells_diff(base_cells, local_cells)
    remote_diff = cells_diff(base_cells, remote_cells)
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

    # By diffing the two diffs, we find *changes* that are
    # on the local branch, the remote branch, or both.
    # We arbitrarily choose the "local" branch to be the "before"
    # and the "remote" branch to be the "after" in the diff algorithm.
    # Therefore:
    # If a change is "deleted", that means that it occurs only on
    # the local branch. If a change is "added" that means it occurs only on
    # the remote branch. If a change is "unchanged", that means it occurs
    # in both branches. Either the same addition or same deletion occurred in
    # both branches, or the cell was not changed in either branch.
    diff_of_diffs = diff.diff(local_diff, remote_diff)

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
    base['worksheets'][0]['cells'] = list(it.chain.from_iterable(rows))

    base['metadata']['nbdiff-type'] = 'merge'

    return base


def diff_result_to_cell(item):
    '''diff.diff returns a dictionary with all the information we need,
    but we want to extract the cell and change its metadata.'''
    state = item['state']
    cell = item['value'].data
    cell['metadata'] = {'state': state}
    return cell


def cells_diff(before_cells, after_cells):
    '''Diff two arrays of cells.'''
    before_comps = [CellComparator(cell) for cell in before_cells]
    after_comps = [CellComparator(cell) for cell in after_cells]
    diff_result = diff.diff(before_comps, after_comps)
    return diff_result
