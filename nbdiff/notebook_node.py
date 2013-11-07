__author__ = 'root'


class NotebookNode(object):
    def add_status(self, status):
        setattr(self, "status", status)
