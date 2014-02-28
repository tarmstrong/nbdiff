import IPython.nbformat.current as current


class NotebookParser:

    #param:
    #json_data: a file-like object with a read() method.
    def parse(self, json_data):
        data = current.read(json_data, 'ipynb')
        json_data.close()
        return data
    
    #param:
    #json_data_string: raw unicode string
    def parseString(self, json_data_string):
        return current.reads(json_data_string, 'ipynb')
       
