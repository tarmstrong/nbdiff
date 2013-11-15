__author__ = 'root'


class CellComparator():

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.equal(self.data, other.data)

    def equal(self, cell1, cell2):
        if not cell1["cell_type"] == cell2["cell_type"]:
            return False
        if self.istextcell(cell1) and self.istextcell(cell2):
            return cell1["source"] == cell2["source"]
        else:
            equallanguage = cell1["language"] == cell2["language"]
            equalinput = cell1["input"] == cell2["input"]
            equaloutputs = self.equaloutputs(cell1["outputs"], cell2["outputs"])
            return equallanguage and equalinput and equaloutputs

    def istextcell(self, cell):
        return "source" in cell

    def equaloutputs(self, output1, output2):
        if not len(output1) == len(output2):
            return False
        for i in range(0, len(output1)):
            if not output1[i] == output2[i]:
                return False
        return True
