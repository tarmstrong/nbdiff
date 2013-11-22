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
    diff_of_diffs = diff.diff(local_diff, remote_diff)
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
    for item in diff_of_diffs:
        state = item['state']
        cell = copy.deepcopy(diff_result_to_cell(item['value']))
        if state == 'deleted':
            if cell['metadata']['state'] == 'unchanged':
                continue
            # This change is on the left.
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
            cell['metadata']['side'] = 'remote'
            if cell['metadata']['state'] == 'unchanged':
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
            # This change is on the right.
            current_row = [
                local_cell,
                base_cell,
                cell,
            ]
        elif state == 'unchanged':
            cell1 = copy.deepcopy(cell)
            cell3 = copy.deepcopy(cell)
            if cell['metadata']['state'] == 'deleted' \
                    or cell['metadata']['state'] == 'unchanged':
                cell2 = copy.deepcopy(cell)
                cell2['metadata']['state'] = 'unchanged'
            else:
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

    base['worksheets'][0]['cells'] = list(it.chain.from_iterable(rows))
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
