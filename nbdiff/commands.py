'''
Entry points for the nbdiff package.
'''
import subprocess
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
        notebook1 = x.parse(open(args.notebook[0]))
        notebook2 = x.parse(open(args.notebook[1]))
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
    length = len(args.notebook)
    if length == 3:
        parser = NotebookParser()
        nb_local = parser.parse(open(args.notebook[0]))
        nb_base = parser.parse(open(args.notebook[1]))
        nb_remote = parser.parse(open(args.notebook[2]))
    elif length == 0:
        output = subprocess.check_output("git ls-files --unmerged")
        output_array = [line.split() for line in output.splitlines()]
        hash_array = []
        i = 0
        for line in output_array:
            hash = line[1]
            hash_array[i] = hash
            i += 1
        nb_local = hash_array[0]
        nb_base = hash_array[1]
        nb_remote = hash_array[2]
    pre_merged_notebook = notebook_merge(nb_local, nb_base, nb_remote)

