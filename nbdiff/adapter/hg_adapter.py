__author__ = 'root'

import hglib
import os
import StringIO

from .vcs_adapter import VcsAdapter
from .vcs_adapter import NoVCSError

# A deliberate copy of GitAdapter's error message:
ERROR_MSG = ("fatal: Not a hg  repository"
             "(or any of the parent directories): .hg")


class HgAdapter(VcsAdapter):

    def __init__(self):

        try:
            hglib.open(os.getcwd())
        except Exception:
            #  This is probably bad practice
            #  Maybe we should not assume that every Exception
            # is thrown because a hg repo can't be found.
            # TODO: check if this assumption is correct
            raise NoVCSError(ERROR_MSG)

    def get_modified_notebooks(self):
        # initialize the mercurial client:
        client = hglib.open(os.getcwd())
        nb_diff = []
        for st, path in client.status(all=True):
            # if the file has been modified since last commit:
            if st == 'M':
                abspath = os.path.abspath(path)  # is this needed?
                current_local_notebook = open(abspath)
                #  Unlike 'git ls-files', client.cat returns the file contents
                # as a plain string. To mantain compatibility with GitAdapter,
                # we have to supply the string as a file-like stream.
                #  A StringIO object behaves as a file handle and can be used
                # for this purpose.
                committed_notebook = StringIO.StringIO(client.cat([abspath]))

                nb_diff.append((current_local_notebook,
                                committed_notebook,
                                path))

        return super(HgAdapter, self).filter_modified_notebooks(nb_diff)

    def get_unmerged_notebooks(self):
        pass

    def stage_file(self, file, contents=None):
        pass
