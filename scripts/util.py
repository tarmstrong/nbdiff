import os
import subprocess

def copy_example_files(fname, root, folders, vcs_cmd='git', add=True):
    for nb in folders:
        target_fname = 'test-{id}.ipynb'.format(id=nb)
        with open(target_fname, 'w') as f:
            ipynb_path = os.path.join(root, nb, fname)
            f.write(open(ipynb_path).read())
            if add:
                subprocess.check_output([vcs_cmd, 'add', target_fname])

