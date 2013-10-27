'''
Entry points for the nbdiff package.
'''
import argparse


def diff():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 2 arguments
    # if 0, use version control (unstaged changes)
    # if 2, use the files.
    print ('Arguments received: {}'.format(args))


def merge():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', nargs='*')
    args = parser.parse_args()
    # TODO take 0 or 3 arguments.
    # if 0, use version control
    # if 3, use the files.
    print ('Arguments received: {}'.format(args))
