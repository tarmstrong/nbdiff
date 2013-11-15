__author__ = 'root'

import json
from comparable import CellComparator


class NotebookParser:

    def parse(self, path):
        json_data = open(path)
        data = json.load(json_data)
        json_data.close()
        return data
