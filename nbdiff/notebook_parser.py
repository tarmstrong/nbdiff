import IPython.nbformat.current as current


class NotebookParser(object):
    """Parser for IPython Notebook files."""
    def parse(self, json_data):
        """Parse a notebook .ipynb file.

        Parameters
        ----------
        json_data : file
            A file handle for an .ipynb file.

        Returns
        -------
        nb : An IPython Notebook data structure.
        """
        data = current.read(json_data, 'ipynb')
        json_data.close()
        return data

    # param:
    # json_data_string: raw unicode string
    def parseString(self, json_data_string):
        return current.reads(json_data_string, 'ipynb')
