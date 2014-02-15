import IPython.nbformat.current as current


class NotebookParser:

    def parse(self, json_data):
        data = current.read(json_data, 'ipynb')
        json_data.close()
        return data
