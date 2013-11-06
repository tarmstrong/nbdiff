__author__ = 'root'

import json
from notebookNode import NotebookNode


class NotebookParser:

    def __init__(self):
        self.data = None

    def load(self, path):
        json_data = open(path)
        self.data = json.load(json_data)
        json_data.close()

    def parse(self, path):
        self.load(path)
        nb = NotebookNode(self.data)
        cells = nb.worksheets[0]["cells"]
        nb.__init__({"worksheets": [NotebookNode({"cells": cells})]})
        cell_list = self.as_cells(nb.worksheets[0].cells)
        nb.__init__({"worksheets": cell_list})
        #self.recursive(self.data, nb)
        return nb

    def as_cells(self, worksheet):
        cell_list = []
        for item in worksheet:
            cell_list.append(NotebookNode(item))
        return cell_list

    def recursive(self, item, notebook_node):
        if type(item) is dict:
            for key in item:
                if type(item[key]) is list:
                    notebook_node.__init__(**{key: self.recursive(item[key])})
                elif type(item[key]) is str or type(item[key]) is int:
                    NotebookNode(**{key: item[key]})
                else:
                    NotebookNode(**{key: self.recursive(item[key])})
        elif type(item) is list:
            for it in item:
                self.recursive(it)


    #def ispair(self, item):
        #return type(item) is dict and len(item) == 1 and (type(list(item.values())[0]) is str or type(list(item.values())[0]) is int)
          # and (type(item.values()[0]) is str or int)

x = NotebookParser()
notebook = x.parse("/home/bobi/GPTutorial.ipynb")