__author__ = 'root'

import json


class NotebookNode(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)