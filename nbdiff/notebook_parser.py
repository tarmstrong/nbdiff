__author__ = 'root'

import json
from notebookNode import NotebookNode

primitive = (int, str, bool)


def isPrimitive(val):
    return isinstance(val, primitive)


class NotebookParser:

    def __init__(self):
        self.data = None

    def load(self, path):
        json_data = open(path)
        self.data = json.load(json_data)
        json_data.close()

    def parse(self, path):
        self.load(path)
        nb = NotebookNode()
        self.recursive(self.data, nb)
        return nb

    def recursive(self, item, notebook_node):
        if type(item) is dict:
            for key in item:
                if type(item[key]) is list:
                    array = []
                    setattr(notebook_node, key, array)
                    self.recursive(item[key], array)
                elif isPrimitive(item[key]):
                    setattr(notebook_node, key, item[key])
                else:
                    node = NotebookNode()
                    setattr(notebook_node, key, node)
                    self.recursive(item[key], node)
        elif type(item) is list:
            for it in item:
                if isPrimitive(it):
                    notebook_node.append(it)
                else:
                    node = NotebookNode()
                    notebook_node.append(node)
                    self.recursive(it, node)

x = NotebookParser()
notebook = x.parse("/home/bobi/Part 5 - Rich Display System.ipynb")
