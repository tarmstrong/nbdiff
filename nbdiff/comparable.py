__author__ = 'root'


class CellComparator():

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.equal(self.data, other.data)

    def equal(self, cell1, cell2):
        if not cell1["cell_type"] == cell2["cell_type"]:
            return False
        if cell1["cell_type"] == "heading":
            return cell1["source"] == cell2["source"] and \
                cell1["level"] == cell2["level"]
        elif self.istextcell(cell1):
            return cell1["source"] == cell2["source"]
        else:
            eqlanguage = cell1["language"] == cell2["language"]
            eqinput = cell1["input"] == cell2["input"]
            eqoutputs = self.equaloutputs(cell1["outputs"], cell2["outputs"])
            return eqlanguage and eqinput and eqoutputs

    def istextcell(self, cell):
        return "source" in cell

    def equaloutputs(self, output1, output2):
        if not len(output1) == len(output2):
            return False
        for i in range(0, len(output1)):
            if not output1[i] == output2[i]:
                return False
        return True
