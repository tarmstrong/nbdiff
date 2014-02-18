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

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]

folder_name = "merge-conflict-testfolder-{}".format(randpart)
os.mkdir(folder_name)
os.chdir(folder_name)
print subprocess.check_output('git init'.split())
with open('test.ipynb', 'w') as f:
    f.write(open('../example.ipynb').read())

print subprocess.check_output('git add test.ipynb'.split())
print subprocess.check_output(['git', 'commit', '-am', 'b'])

print subprocess.check_output('git checkout -b your-friends-branch'.split())

with open('test.ipynb', 'w') as f:
    f.write(open('../example-remote.ipynb').read())

print subprocess.check_output(['git', 'commit', '-am', 'r'], stderr=sys.stdout)

print subprocess.check_output('git checkout master'.split())
with open('test.ipynb', 'w') as f:
    f.write(open('../example-local.ipynb').read())

print subprocess.check_output(['git', 'commit', '-am', 'l'])


try:
    print 'Attempting merge in {}'.format(folder_name)
    print subprocess.check_output('git merge your-friends-branch'.split())
except:
    print 'Conflict!'


