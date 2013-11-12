__author__ = 'root'

from abc import ABCMeta, abstractmethod


class MyComparable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def equal(self, cell1, cell2):
        pass


class CellComparator(MyComparable):

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        self.equal(self.data, other)

#    def equalworksheets(self, worksheet1, worksheet2):
#        return [(i, j) for i, j in zip(worksheet1["cells"], worksheet2["cells"]) if not self.equal(i, j)]

    def equal(self, cell1, cell2):
        if not cell1["cell_type"] == cell2["cell_type"]:
            return False
        if self.istextcell(cell1) and self.istextcell(cell2):
            return cell1["source"] == cell2["source"]
        else:
            return cell1["language"] == cell2["language"] and cell1["input"] == cell2["input"] \
                and not [i for i, j in zip(cell1["outputs"], cell2["outputs"])
                         if not self.equaloutputs(cell1["outputs"], cell2["outputs"])]

    def istextcell(self, cell):
        return "source" in cell

    def equaloutputs(self, outputs1, outputs2):
        return not [i for i, j in zip(outputs1, outputs2)
                         if not i == j]