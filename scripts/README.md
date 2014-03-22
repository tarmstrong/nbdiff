# Testing scripts for NBDiff

## `make_merge_conflict.py` and `make_merge_conflict_hg.py`

This script initializes a git repository and causes a merge conflict in a file called `test.ipynb`.

Example run:

```
$ python make_merge_conflict.py

Switched to a new branch 'your-friends-branch'
Switched to branch 'master'
Attempting merge in:
merge-conflict-testfolder-fb2d
Conflict!
merge-conflict-testfolder-fb2d
```

This creates a folder called `merge-conflict-testfolder-fb2d`.

The following shows how to change into that directory and run `nbmerge`.

```
$ cd merge-conflict-testfolder-fb2d/

$ ls
test-0.ipynb  test-2.ipynb
test-1.ipynb  test-3.ipynb

$ git status
# On branch master
# You have unmerged paths.
#   (fix conflicts and run "git commit")
#
# Unmerged paths:
#   (use "git add <file>..." to mark resolution)
#
#	both modified:      test-0.ipynb
#	both modified:      test-1.ipynb
#	both modified:      test-2.ipynb
#	both modified:      test-3.ipynb
#
no changes added to commit (use "git add" and/or "git commit -a")


$ nbmerge
There was a problem parsing the following notebook files:
test-2.ipynb
test-3.ipynb
 * Running on http://127.0.0.1:5000/
Created new window in existing browser session.
```

`test-0.ipynb` and `test-1.ipynb` are valid notebook files and will open in your browser.

`test-2.ipynb` and `test-3.ipynb` are not valid notebook files and will print an error message to your console. 

`make_merge_conflict_hg.py` does the same thing but with a mercurial repository.
TODO explain how to run nbmerge with mercurial.

## `make_diff.py`

This script initializes a git repository, adds a test notebook file, and then modifies it.

```
$ python make_diff.py
Diffable notebook available in folder: 
merge-diff-testfolder-b79a
```

Change into the directory called `merge-diff-testfolder-b79a` 

```
$ cd merge-diff-testfolder-b79a/
$ ls
test-0.ipynb  test-2.ipynb  test-4.ipynb
test-1.ipynb  test-3.ipynb  test-5.ipynb
```

Run `nbdiff` to see a diff of the notebooks:

```
$ nbdiff
There was a problem parsing the following notebook files:
test-4.ipynb
test-3.ipynb
test-5.ipynb
 * Running on http://127.0.0.1:5000/
Created new window in existing browser session.
```

`test-0.ipynb` `test-1.ipynb` and `test-2.ipynb` are valid notebook files and will open in your browser.

`test-3.ipynb` `test-4.ipynb` and `test-5.ipynb` are not valid notebook files and will print an error message to your console. 

#For manual testing of example notebooks 

## Diff notebook examples - `example-notebooks/diff/`

```
$ cd example-notebooks/diff/
$ ls
0  1  2  3  4  5
```

Each of the folders contains a pair of notebooks that can be diffed.

Navigate to one of the folders and run the command `nbdiff before.ipynb after.ipynb`

Example run:

```
$ cd 1
$ ls
after.ipynb  before.ipynb
```
Now run the command to diff the two notebooks.

```
$ nbdiff before.ipynb after.ipynb 
 * Running on http://127.0.0.1:5000/
Created new window in existing browser session.
```

####Expected Results for all example diff notebooks:

**0:** `before.ipynb` and `after.ipynb` are both valid notebooks
   * `before.ipynb` has some deleted cells
   * `after.ipynb` has an added cell
   *  There are unchanged cells
   *  There are modified headers

**1:** `before.ipynb` and `after.ipynb` are both valid notebooks
   * `before.ipynb` has some deleted cells
   * `before.ipynb` has a deleted graph
   * `after.ipynb` has an added header 
   *  There are unchanged cells
   *  There are unchanged graphs

**2:** `before.ipynb` and `after.ipynb` are both valid notebooks
   * `before.ipynb` has some deleted cells
   * `before.ipynb` has some deleted lines 
   * `after.ipynb` has some added cells
   * `after.ipynb` has some added lines 

**3:** `before.ipynb` is a valid notebook and `after.ipynb` is an invalid notebook

**4:** `before.ipynb` is an invalid notebook and `after.ipynb` is a valid notebook

**5:** `before.ipynb` and `after.ipynb` are both invalid notebooks


## Merge notebook examples - `example-notebooks/merge/`

```
$ cd example-notebooks/merge/
$ ls
0  1  2  3
```

Each of the folders contains an example of a merge conflict. 

Three notebooks are supplied in each folder: `local.ipynb` `base.ipynb` `remote.ipynb`

Navigate to one of the folders and run the command `nbmerge local.ipynb base.ipynb remote.ipynb`

Example run:

```
$ cd 0
$ ls
base.ipynb  local.ipynb  remote.ipynb
```
Now run the command to diff the two notebooks.

```
$ nbmerge local.ipynb base.ipynb remote.ipynb
 * Running on http://127.0.0.1:5000/
Created new window in existing browser session.
```

####Expected Results for all example merge notebooks:

**0:** `local.ipynb` `base.ipynb` `remote.ipynb` are all valid notebooks
   * `local.ipynb` has an added cell
   * `remote.ipynb` has an added cell 
   * `remote.ipynb` has a deleted cell

**1:** `local.ipynb` `base.ipynb` `remote.ipynb` are all valid notebooks
   * `local.ipynb` has some deleted headers
   * `local.ipynb` has some added headers
   * `local.ipynb` has some deleted cells
   * `local.ipynb` has some added cells
   * `remote.ipynb` has some deleted headers
   * `remote.ipynb` has some deleted cells
   * `remote.ipynb` has some added cells

**2:** `local.ipynb` `base.ipynb` are valid notebooks and `remote.ipynb` is an invalid notebook

**3:** `remote.ipynb` `base.ipynb` are valid notebooks and `local.ipynb` is an invalid notebook

**4:** `local.ipynb` `remote.ipynb` are valid notebooks and `base.ipynb` is an invalid notebook

**5:** `local.ipynb` `base.ipynb` `remote.ipynb` are all invalid notebooks




