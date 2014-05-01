__author__ = 'root'

import re


class VcsAdapter(object):

    def get_modified_notebooks(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def filter_modified_notebooks(self, file_hooks):
        modified_notebooks = []
        for item in file_hooks:
            if re.search('.ipynb$', item[2]):
                modified_notebooks.append(item)

        return modified_notebooks

    def get_unmerged_notebooks(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def filter_unmerged_notebooks(self, file_hooks):
        unmerged_notebooks = []
        for item in file_hooks:
            if re.search('.ipynb$', item[3]):
                unmerged_notebooks.append(item)

        return unmerged_notebooks

    def stage_file(self, file, contents=None):
        raise NotImplementedError("Subclass must implement abstract method")


class NoVCSError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
