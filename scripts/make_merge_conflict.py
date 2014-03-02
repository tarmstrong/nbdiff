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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mercurial', '-m', action='store_true', default=False)

args = parser.parse_args()
MERCURIAL = args.mercurial

VCS_CMD = MERCURIAL and 'hg' or 'git'

SCRIPTS_DIR = os.path.realpath(os.path.dirname(__file__))
EXAMPLE_NOTEBOOKS = os.path.join(SCRIPTS_DIR, 'example-notebooks/merge/')

example_merge_notebooks = os.listdir(EXAMPLE_NOTEBOOKS)

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]
folder_name = "merge-conflict-testfolder-{}".format(randpart)

os.mkdir(folder_name)
os.chdir(folder_name)

subprocess.check_output([VCS_CMD, 'init'])

copy_example_files('base.ipynb', EXAMPLE_NOTEBOOKS, example_merge_notebooks, vcs_cmd=VCS_CMD)

if MERCURIAL:
    subprocess.check_output(['hg', 'commit', '-A', '-m', 'b'])
    subprocess.check_output('hg bookmark main'.split())
    subprocess.check_output('hg bookmark friend'.split())
    subprocess.check_output('hg update friend'.split())
else:
    subprocess.check_output(['git', 'commit', '-am', 'b'])
    subprocess.check_output('git checkout -b your-friends-branch'.split())


copy_example_files('remote.ipynb', EXAMPLE_NOTEBOOKS, example_merge_notebooks, vcs_cmd=VCS_CMD)

if MERCURIAL:
    subprocess.check_output(['hg', 'commit', '-A', '-m', 'r'], stderr=sys.stdout)
    subprocess.check_output('hg update main'.split())
else:
    subprocess.check_output(['git', 'commit', '-am', 'r'], stderr=sys.stdout)
    subprocess.check_output('git checkout master'.split())

copy_example_files('local.ipynb',EXAMPLE_NOTEBOOKS,  example_merge_notebooks, vcs_cmd=VCS_CMD)

if MERCURIAL:
    subprocess.check_output(['hg', 'commit', '-A', '-m', 'l'])
else:
    subprocess.check_output(['git', 'commit', '-am', 'l'])


try:
    print 'Attempting merge in {}'.format(folder_name)
    if MERCURIAL:
        subprocess.check_output('hg merge friend -t nbmerge'.split())
    else:
        subprocess.check_output('git merge your-friends-branch'.split())
except:
    print 'Conflict!'
    print folder_name


