#!/usr/bin/env python

# Tavish Armstrong (c) 2013
#
# make_merge_conflict.py
#
# Make a new directory, initialize a hg repository within, and cause a merge conflict.
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
print subprocess.check_output('hg init'.split())
with open('test.ipynb', 'w') as f:
    f.write(open('../example.ipynb').read())

print subprocess.check_output('hg add test.ipynb'.split())
print subprocess.check_output(['hg', 'commit', '-A', '-m', 'b'])

print subprocess.check_output('hg bookmark main'.split())
print subprocess.check_output('hg bookmark friend'.split())
print subprocess.check_output('hg update friend'.split())

with open('test.ipynb', 'w') as f:
    f.write(open('../example-remote.ipynb').read())

print subprocess.check_output(['hg', 'commit', '-A', '-m', 'r'], stderr=sys.stdout)

print subprocess.check_output('hg update main'.split())
with open('test.ipynb', 'w') as f:
    f.write(open('../example-local.ipynb').read())

print subprocess.check_output(['hg', 'commit', '-A', '-m', 'l'])


try:
    print 'Attempting merge in {}'.format(folder_name)
    print subprocess.check_output('hg merge friend -t nbmerge'.split())
except:
    print 'Conflict!'


