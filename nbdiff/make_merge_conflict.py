# Tavish Armstrong (c) 2013
#
# make_merge_conflict.py
#
# Make a new directory, initialize a git repository within,
# and cause a merge conflict.
# Yes. On purpose.

import os
import subprocess
import random
import hashlib

randpart = hashlib.sha1(str(random.random())).hexdigest()[:4]

folder_name = "merge-conflict-testfolder-{}".format(randpart)
os.mkdir(folder_name)
os.chdir(folder_name)
print subprocess.check_output('git init'.split())
with open('test.txt', 'w') as f:
    f.write("\n".join("123456"))

print subprocess.check_output('git add test.txt'.split())
print subprocess.check_output(['git', 'commit', '-am', '"Base commit"'])
print subprocess.check_output('git checkout -b your-friends-branch'.split())

with open('test.txt', 'w') as f:
    f.write("\n".join("133456"))

print subprocess.check_output(['git', 'commit', '-am', '"Friend commit"'])
print subprocess.check_output('git checkout master'.split())

with open('test.txt', 'w') as f:
    f.write("\n".join("173456"))

print subprocess.check_output(['git', 'commit', '-am', '"My commit"'])
print subprocess.check_output('git merge your-friends-branch'.split())
