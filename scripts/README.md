# Testing scripts for NBDiff

## `make_merge_conflict.py` and `make_merge_conflict_hg.py`

This script initializes a git repository and causes a merge conflict in a file called `test.ipynb`.

Example run:

```
$ python make_merge_conflict.py

Switched to a new branch 'your-friends-branch'
Switched to branch 'master'
Initialized empty Git repository in /home/tavish/capstone/nbdiff/scripts/merge-conflict-testfolder-fe14/.git/


[master (root-commit) 8827668] b
 1 file changed, 56 insertions(+)
 create mode 100644 test.ipynb


[your-friends-branch 9bdfb5f] r
 1 file changed, 2 insertions(+), 3 deletions(-)


[master 7a1f33e] l
 1 file changed, 20 insertions(+)

Attempting merge in merge-conflict-testfolder-fe14
Conflict!
```

This creates a folder called `merge-conflict-testfolder-fe14`.

The following shows how to change into that directory and run `nbmerge`.

```
$ cd merge-conflict-testfolder-fe14/

$ ls
test.ipynb

$ git status
# On branch master
# You have unmerged paths.
#   (fix conflicts and run "git commit")
#
# Unmerged paths:
#   (use "git add <file>..." to mark resolution)
#
#	both modified:      test.ipynb
#
no changes added to commit (use "git add" and/or "git commit -a")

$ nbmerge
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

`make_merge_conflict_hg.py` does the same thing but with a mercurial repository.
TODO explain how to run nbmerge with mercurial.

## `make_diff.py`

This script initializes a git repository, adds a test notebook file, and then modifies it.

```
$ python make_diff.py

Initialized empty Git repository in /home/tavish/capstone/nbdiff/scripts/merge-diff-testfolder-7bee/.git/


[master (root-commit) 11b59ef] b
 1 file changed, 56 insertions(+)
 create mode 100644 test.ipynb

Diffable notebook available in folder: merge-diff-testfolder-7bee
```

Change into the directory called `merge-diff-testfolder-7bee` and run `nbdiff` to see a diff of the notebook:

```
$ cd merge-diff-testfolder-7bee
$ nbdiff
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```
