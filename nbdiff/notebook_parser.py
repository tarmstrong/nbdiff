__author__ = 'root'

import json
from notebook_node import NotebookNode

primitive = (int, str, bool)


def is_primitive(val):
    return isinstance(val, primitive)


class NotebookParser:

    def parse(self, path):
        json_data = open(path)
        data = json.load(json_data)
        json_data.close()
        nb = NotebookNode()
        self.deserialize(data, nb)
        return nb

    def deserialize(self, item, notebook_node):
        if type(item) is dict:
            for key in item:
                if type(item[key]) is list:
                    array = []
                    setattr(notebook_node, key, array)
                    self.deserialize(item[key], array)
                elif is_primitive(item[key]):
                    setattr(notebook_node, key, item[key])
                else:
                    node = NotebookNode()
                    setattr(notebook_node, key, node)
                    self.deserialize(item[key], node)
        elif type(item) is list:
            for it in item:
                if is_primitive(it):
                    notebook_node.append(it)
                else:
                    node = NotebookNode()
                    notebook_node.append(node)
                    self.deserialize(it, node)

x = NotebookParser()
notebook = x.parse("/home/lenovo/Part 5 - Rich Display System.ipynb")
