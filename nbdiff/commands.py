'''
Entry points for the nbdiff package.
'''
import argparse
from .notebook_parser import NotebookParser
from .comparable import CellComparator
from . import diff as differ
import json


def diff():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 2 arguments
    # if 0, use version control (unstaged changes)
    # if 2, use the files.
    length = len(args.notebook)
    if length == 2:
        x = NotebookParser()
        notebook1 = x.parse(args.notebook[0])
        notebook2 = x.parse(args.notebook[1])
        notequal = []
        nb1_cells = [CellComparator(c) for c in notebook1['worksheets'][0]['cells']]
        nb2_cells = [CellComparator(c) for c in notebook2['worksheets'][0]['cells']]
        result = differ.diff(nb1_cells, nb2_cells)
        notebook1['worksheets'][0]['cells'] = [
            dict(r['value'].data.items() + {'metadata': {'state': r['state']}}.items())
            for r in result
        ]
        print json.dumps(notebook1)


def merge():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 3 arguments.
    # if 0, use version control
    # if 3, use the files.
    print('Arguments received: {}'.format(args))
