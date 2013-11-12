__author__ = 'root'

import json
from notebook_node import NotebookNode
from comparable import CellComparator

primitive = (int, str, bool)


def is_primitive(val):
    return isinstance(val, primitive)


class NotebookParser:

    def parse(self, path):
        json_data = open(path)
        data = json.load(json_data)
        json_data.close()
        nb = NotebookNode()
        #self.deserialize(data, nb)
        return data

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
notebook = x.parse("Part_5_-_Rich_Display_System.ipynb")
notebook2 = x.parse("Part_5_-_Rich_Display_System_(changed).ipynb")
comparator = CellComparator()

notequal = comparator.equalworksheets(notebook["worksheets"][0], notebook2["worksheets"][0])
notequal[0][0]["metadata"]["status"] = "changed"
notequal[0][1]["metadata"]["status"] = "changed"

print (len(notequal))