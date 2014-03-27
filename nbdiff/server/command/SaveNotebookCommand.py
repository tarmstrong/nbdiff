from . import BaseCommand
from flask import make_response
from IPython.nbformat import current
from unicodedata import normalize


class SaveNotebookCommand(BaseCommand):

    def process(self, request, filename, db_session):
        # format for notebook.
        format = u'json'
        data = request.form['download_data']

        try:
            # read notebook and format it.
            nb = current.reads(data.decode('utf-8'), format)
        except:
            return "Unable to save notebook. Invalid JSON data"

        # if notebook has a name we use it else use a generic name
        try:
            name = nb.metadata.name
        except:
            name = "mergedNotebook"
            nb.metadata.name = name

        name = normalize('NFC', nb.metadata.name)

        # uses ipython's current ipynb formatting.
        notebook_formatted = current.writes(nb, format)

        # make a file download response
        response = make_response(notebook_formatted)
        header = "attachment; filename=mergedNotebook.ipynb"
        response.headers["Content-Type"] = "text/plain"
        response.headers["Content-Disposition"] = header

        return response


def newInstance():
    return SaveNotebookCommand()
