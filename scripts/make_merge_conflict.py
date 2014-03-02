#!/usr/bin/env python

# Tavish Armstrong (c) 2013
#
# make_merge_conflict.py
#
# Make a new directory, initialize a git repository within, and cause a merge conflict.
# Yes. On purpose.

import os
import subprocess
import random
import hashlib
import sys
from util import copy_example_files

SCRIPTS_DIR = os.path.realpath(os.path.dirname(__file__))
EXAMPLE_NOTEBOOKS = os.path.join(SCRIPTS_DIR, 'example-notebooks/merge/')

example_merge_notebooks = os.listdir(EXAMPLE_NOTEBOOKS)

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]
folder_name = "merge-conflict-testfolder-{}".format(randpart)

os.mkdir(folder_name)
os.chdir(folder_name)

subprocess.check_output('git init'.split())


copy_example_files('base.ipynb',EXAMPLE_NOTEBOOKS, example_merge_notebooks)
subprocess.check_output(['git', 'commit', '-am', 'b'])

subprocess.check_output('git checkout -b your-friends-branch'.split())

copy_example_files('remote.ipynb',EXAMPLE_NOTEBOOKS, example_merge_notebooks)

subprocess.check_output(['git', 'commit', '-am', 'r'], stderr=sys.stdout)

subprocess.check_output('git checkout master'.split())

copy_example_files('local.ipynb',EXAMPLE_NOTEBOOKS,  example_merge_notebooks)

subprocess.check_output(['git', 'commit', '-am', 'l'])


try:
    print 'Attempting merge in {}'.format(folder_name)
    print subprocess.check_output('git merge your-friends-branch'.split())
except:
    print 'Conflict!'
    print folder_name


