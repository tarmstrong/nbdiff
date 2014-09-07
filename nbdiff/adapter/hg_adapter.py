__author__ = 'root'

import hglib
import os
import StringIO

from .vcs_adapter import VcsAdapter
from .vcs_adapter import NoVCSError

# A deliberate copy of GitAdapter's error message:
ERR_MSG = "fatal: Not a hg  repository (or any of the parent directories): .hg"


##############################################################
# Funcions to search the filesystem for a hg repository
# the search is from the current directory to the root.
##############################################################
# TODO: is this portable?
def isroot(path):
    return os.path.normpath(path) == os.path.abspath(os.sep)


def isempty(path):
    return os.path.normpath(path) == ''


def walkback(path, from_parent=False):
    # Handle redundant patterns and separators like '/home/user/..'
    normpath = os.path.normpath(path)

    if os.path.isdir(path):
        if from_parent:
            directory = os.path.dirname(normpath)
        else:
            directory = normpath
    else:
        directory = os.path.dirname(normpath)
    #  Loop until either:
    #   1) we have reached the root of the filesystem
    #      (the end of an absolute path)
    #   2) we have reached an empty path
    #      (the end of a relative path)
    #
    #  The empty path or the path to the root are still yielded,
    # (only once, since we interrupt the loop)
    while True:
        yield directory
        if isroot(directory) or isempty(directory):
            #   Now that we have already yielded the
            # path to the root or the empty path, we
            # terminate the loop.
            #   This is done to make sure these paths
            # are yielded only once, instead of entering
            # an infinite cycle.
            return
        directory = os.path.dirname(directory)


# Walks "back" into the root of the filesystem
# to try to find a hg repository
def get_hlib_client_and_path(directory):
    for dirpath in walkback(directory):
        try:
            return hglib.open(dirpath), dirpath
        except Exception:
            pass
    raise NoVCSError(ERR_MSG)


class HgAdapter(VcsAdapter):

    def __init__(self):
        get_hlib_client_and_path(os.getcwd())

    def get_modified_notebooks(self):
        # initialize the mercurial client:
        client, repopath = get_hlib_client_and_path(os.getcwd())
        nb_diff = []
        for st, path in client.status(all=True):
            # if the file has been modified since last commit:
            if st == 'M':
                # returned by client.status is relative to the repo location
                abspath = os.path.join(repopath, path)
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
