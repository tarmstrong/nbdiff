__author__ = 'root'

import re


class VcsAdapter(object):

    def get_modified_files(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_modified_notebooks(self, file_hooks):
        modified_notebooks = []
        for item in file_hooks:
            if re.search('.ipynb$', item[2]):
                three_tuple = (item[0], item[1], item[2])
                modified_notebooks.append(three_tuple)

        return modified_notebooks

    def get_unmerged_files(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_unmerged_notebooks(self, file_hooks):
        unmerged_notebooks = []
        for item in file_hooks:
            if re.search('.ipynb$', item[3]):
                four_tuple = (item[0], item[1], item[2], item[3])
                unmerged_notebooks.append(four_tuple)

        return unmerged_notebooks

    def stage_file(self, file, contents=None):
        raise NotImplementedError("Subclass must implement abstract method")
