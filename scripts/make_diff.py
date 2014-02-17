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

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]

folder_name = "merge-diff-testfolder-{}".format(randpart)
os.mkdir(folder_name)
os.chdir(folder_name)
print subprocess.check_output('git init'.split())

# create initial version of notebook
with open('test.ipynb', 'w') as f:
    f.write(open('../example.ipynb').read())

print subprocess.check_output('git add test.ipynb'.split())
print subprocess.check_output(['git', 'commit', '-am', 'b'])

# overwrite with changes.
with open('test.ipynb', 'w') as f:
    f.write(open('../example-local.ipynb').read())

print 'Diffable notebook available in folder: ' + folder_name

