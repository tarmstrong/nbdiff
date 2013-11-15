'''
Entry points for the nbdiff package.
'''
import argparse
from notebook_parser import NotebookParser
from comparable import CellComparator


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
        for i in range(0, len(notebook1["worksheets"][0]["cells"])):
            cell1 = notebook1['worksheets'][0]['cells'][i]
            cell2 = notebook2['worksheets'][0]['cells'][i]
            if not CellComparator(cell1) == CellComparator(cell2):
                notequal.append((cell1, cell2))
        for cell1, cell2 in notequal:
            print(cell1)
            print(cell2)

    print('Arguments received: {}'.format(args.notebook))


def merge():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 3 arguments.
    # if 0, use version control
    # if 3, use the files.
    print('Arguments received: {}'.format(args))
