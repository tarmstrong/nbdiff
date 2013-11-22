'''
Entry points for the nbdiff package.
'''
import subprocess
import argparse
from merge import notebook_merge
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
    if length == 0:
        output = subprocess.check_output("git ls-files --unmerged".split())
        output_array = [line.split() for line in output.splitlines()]
        hash_array = []
        for line in output_array:
            hash = line[1]
            hash_array.append(hash)
        nb_local = hash_array[0]
        nb_base = hash_array[1]
        nb_remote = hash_array[2]
    elif length == 3:
        parser = NotebookParser()
        local_show = subprocess.Popen(
            ['git', 'show', hash_array[0]],
            stdout=subprocess.PIPE
        )
        nb_local = local_show.stdout
        base_show = subprocess.Popen(
            ['git', 'show', hash_array[1]],
            stdout=subprocess.PIPE
        )
        nb_base = base_show.stdout
        remote_show = subprocess.Popen(
            ['git', 'show', hash_array[2]],
            stdout=subprocess.PIPE
        )
        nb_remote = remote_show.stdout
    pre_merged_notebook = notebook_merge(nb_local, nb_base, nb_remote)
    print pre_merged_notebook
