__author__ = 'root'

import hglib
import os
import StringIO

from .vcs_adapter import VcsAdapter
from .vcs_adapter import NoVCSError

# A deliberate copy of GitAdapter's error message:
ERR_MSG = "fatal: Not a hg  repository (or any of the parent directories): .hg"


def get_hlib_client_and_path():
    try:
        client = hglib.open()
        repopath = client.root()
        return client, repopath
    except Exception:
        raise NoVCSError(ERR_MSG)


class HgAdapter(VcsAdapter):

    def __init__(self):
        get_hlib_client_and_path()

    def get_modified_notebooks(self):
        # initialize the mercurial client:
        client, repopath = get_hlib_client_and_path()
        # Gather unmerged files:
        unmerged = [path for (status, path) in client.resolve(listfiles=True)
                    if status == 'U']
        nb_diff = []
        for status, path in client.status(all=True):
            # if the file has been modified since last commit:
            if status == 'M' and path not in unmerged:
                # returned by client.status is relative to the repo location
                abspath = os.path.join(repopath, path)
                if os.path.exists(abspath):
                    current_local_notebook = open(abspath)
                    #  Unlike 'git ls-files', client.cat returns the file
                    # contents as a plain string. To mantain compatibility
                    # with GitAdapter, we have to supply the string as a
                    # file-like stream. A StringIO object behaves as a file
                    # handle and can be used for this purpose.
                    notebook = client.cat([abspath])
                    committed_notebook = StringIO.StringIO(notebook)

                    nb_diff.append((current_local_notebook,
                                    committed_notebook,
                                    path))

        return super(HgAdapter, self).filter_modified_notebooks(nb_diff)

    def get_unmerged_notebooks(self):
        client, repopath = get_hlib_client_and_path()
        # Gather unmerged files:
        unmerged = [path for (status, path) in client.resolve(listfiles=True)
                    if status == 'U']
        if not unmerged:
            return []

        nb_diff = []

        local_remote_hash = client.identify(id=True).split('+')
        local_hash = local_remote_hash[0]
        remote_hash = local_remote_hash[1]
        base_hash = client.log("ancestor('" + local_hash +
                               "', '" + remote_hash + "')")[0][1]

        for status, path in client.status(all=True):
            if path in unmerged:
                abspath = os.path.join(repopath, path)
                name = os.path.basename(abspath)

                local_nb_str = client.cat([name], rev=local_hash)
                remote_nb_str = client.cat([name], rev=remote_hash)
                base_nb_str = client.cat([name], rev=base_hash)

                local_notebook = StringIO.StringIO(local_nb_str)
                remote_notebook = StringIO.StringIO(remote_nb_str)
                base = StringIO.StringIO(base_nb_str)

                nb_diff.append((local_notebook,
                                base,
                                remote_notebook,
                                abspath))
        return super(HgAdapter, self).filter_unmerged_notebooks(nb_diff)

    def stage_file(self, file, contents=None):
        pass
