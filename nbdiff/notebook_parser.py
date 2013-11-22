__author__ = 'root'

import json


class NotebookParser:

    def parse(self, json_data):
        data = json.load(json_data)
        json_data.close()
        return data
