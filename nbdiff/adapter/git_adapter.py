__author__ = 'root'

import sys
import subprocess
import os
from .vcs_adapter import VcsAdapter
from .vcs_adapter import NoVCSError


class GitAdapter(VcsAdapter):

    def __init__(self):
        is_git_repo = False

        try:
            is_git_repo = subprocess.check_output(
                "git rev-parse --is-inside-work-tree".split()) == "true\n"
        except subprocess.CalledProcessError:
            raise NoVCSError("Git repository not found.")

        if not is_git_repo:
            raise NoVCSError("Git repository not found.")

    def get_modified_notebooks(self):
        # get modified file names
        modified = subprocess.check_output(
            "git ls-files --modified --full-name".split()
        )
        fnames = modified.splitlines()

        if not fnames:
            return []

        # get unmerged file info
        unmerged = subprocess.check_output(
            "git ls-files --unmerged --full-name".split()
        )
        unmerged_array = [line.split() for line in unmerged.splitlines()]

        # get unmerged file names
        unmerged_array_names = [x[3] for x in unmerged_array]

        # ignore unmerged files, get unique names
        fnames = list(set(fnames) - set(unmerged_array_names))

        git_root_path = subprocess.check_output(
            "git rev-parse --show-toplevel".split()
        ).splitlines()[0]

        nb_diff = []
        for name in fnames:
            head_version_show = subprocess.Popen(
                ['git', 'show', 'HEAD:' + name],
                stdout=subprocess.PIPE
            )

            absolute_file_path = os.path.join(git_root_path, name)

            if os.path.exists(absolute_file_path):
                current_local_notebook = open(absolute_file_path)
                committed_notebook = head_version_show.stdout

                nb_diff.append((current_local_notebook, committed_notebook, name))

        return super(GitAdapter, self).filter_modified_notebooks(nb_diff)

    def get_unmerged_notebooks(self):
        output = subprocess.check_output(
            "git ls-files --unmerged --full-name".split()
        )
        output_array = [line.split() for line in output.splitlines()]

        if not output_array:
            return []

        if len(output_array) % 3 != 0:  # TODO should be something else
            sys.stderr.write(
                "Can't find the conflicting notebook. Quitting.\n")
            sys.exit(-1)

        hash_list = []

        for index in xrange(0, len(output_array), 3):
            local_hash = output_array[index + 1][1]
            base_hash = output_array[index][1]
            remote_hash = output_array[index + 2][1]
            file_name = output_array[index][3]
            hash_list.append((local_hash, base_hash, remote_hash, file_name))

        file_hooks = []

        git_root_path = subprocess.check_output(
            "git rev-parse --show-toplevel".split()
        ).splitlines()[0]

        for hash in hash_list:
            local = subprocess.Popen(
                ['git', 'show', hash[0]],
                stdout=subprocess.PIPE
            )
            base = subprocess.Popen(
                ['git', 'show', hash[1]],
                stdout=subprocess.PIPE
            )
            remote = subprocess.Popen(
                ['git', 'show', hash[2]],
                stdout=subprocess.PIPE
            )
            # file_name = hash[3]
            absolute_file_path = os.path.join(git_root_path, hash[3])
            file_hooks.append((local.stdout, base.stdout,
                              remote.stdout, absolute_file_path))

        return super(GitAdapter, self).filter_unmerged_notebooks(file_hooks)

    def stage_file(self, file, contents=None):
        if contents is not None:
            with open(file, 'w') as result_file:
                result_file.write(file)
        command = ["git", "add", file]
        return subprocess.call(command)
