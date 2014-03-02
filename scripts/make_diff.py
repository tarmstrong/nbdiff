#!/usr/bin/env python

# Tavish Armstrong (c) 2013
#
# make_diff.py
#
# Make a new git repository, add a notebook, and then modify it.
# nbdiff should then be able to show a diff.


import os
import subprocess
import random
import hashlib
import sys

SCRIPTS_DIR = os.path.realpath(os.path.dirname(__file__))
EXAMPLE_NOTEBOOKS = os.path.join(SCRIPTS_DIR, 'example-notebooks/diff/')

example_diff_notebooks = os.listdir(EXAMPLE_NOTEBOOKS)

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]

folder_name = "merge-diff-testfolder-{}".format(randpart)
os.mkdir(folder_name)
os.chdir(folder_name)
print subprocess.check_output('git init'.split())


# create initial version of notebooks
for nb in example_diff_notebooks:
    target_fname = 'test-{id}.ipynb'.format(id=nb)
    with open(target_fname, 'w') as f:
        ipynb_path = os.path.join(EXAMPLE_NOTEBOOKS, nb, 'before.ipynb')
        f.write(open(ipynb_path).read())
        print subprocess.check_output(['git', 'add', target_fname])

print subprocess.check_output(['git', 'commit', '-am', 'b'])

for nb in example_diff_notebooks:
    target_fname = 'test-{id}.ipynb'.format(id=nb)
    with open(target_fname, 'w') as f:
        ipynb_path = os.path.join(EXAMPLE_NOTEBOOKS, nb, 'after.ipynb')
        f.write(open(ipynb_path).read())

print 'Diffable notebook available in folder: ' + folder_name

