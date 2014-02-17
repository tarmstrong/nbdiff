__author__ = 'root'

import sys
import subprocess
from .vcs_adapter import VcsAdapter


class GitAdapter(VcsAdapter):

    def get_modified_files(self):
        output = subprocess.check_output("git ls-files --modified".split())
        fnames = output.splitlines()
        fname = fnames[0]  # TODO handle multiple notebooks

        head_version_show = subprocess.Popen(
            ['git', 'show', 'HEAD:' + fname],
            stdout=subprocess.PIPE
        )

        current_local_notebook = open(fname)
        committed_notebook = head_version_show.stdout

        nb_diff = (current_local_notebook, committed_notebook, fname)
        return nb_diff

    def get_unmerged_files(self):
        # TODO error handling.

        output = subprocess.check_output("git ls-files --unmerged".split())
        output_array = [line.split() for line in output.splitlines()]

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

        result_file_hooks = []

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
            file_name = hash[3]
            result_file_hooks.append((local.stdout, base.stdout,
                                      remote.stdout, file_name))

        return result_file_hooks

    def stage_file(self, file, contents=None):
        pass
