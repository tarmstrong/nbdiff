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
from util import copy_example_files

SCRIPTS_DIR = os.path.realpath(os.path.dirname(__file__))
EXAMPLE_NOTEBOOKS = os.path.join(SCRIPTS_DIR, 'example-notebooks/diff/')

example_diff_notebooks = os.listdir(EXAMPLE_NOTEBOOKS)

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]

folder_name = "merge-diff-testfolder-{}".format(randpart)
os.mkdir(folder_name)
os.chdir(folder_name)

subprocess.check_output('git init'.split())


copy_example_files('before.ipynb', EXAMPLE_NOTEBOOKS, example_diff_notebooks)

subprocess.check_output(['git', 'commit', '-am', 'b'])

copy_example_files('after.ipynb',EXAMPLE_NOTEBOOKS, example_diff_notebooks, add=False)

print 'Diffable notebook available in folder: \n' + folder_name

