'''
Entry points for the nbdiff package.
'''
import argparse
from notebook_parser import NotebookParser


def diff():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 2 arguments
    # if 0, use version control (unstaged changes)
    # if 2, use the files.
    #length = len(args.notebook)
    #if length == 0:
        #do
    #elif length == 2:
    #    x = NotebookParser()
    #    x.parse(args.notebook[0])
    #else:
    #    raise ValueError("Number of arguments must be either 0 or 2")

    print('Arguments received: {}'.format(args.notebook))


def merge():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 3 arguments.
    # if 0, use version control
    # if 3, use the files.
    print('Arguments received: {}'.format(args))
