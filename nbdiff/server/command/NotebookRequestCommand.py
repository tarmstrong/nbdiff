from . import BaseCommand
from nbdiff.server.database.nbdiffModel import nbdiffModel
import bitarray


class NotebookRequestCommand(BaseCommand):

    def process(self, request, filename, db_session):

        # query for the notebook in database.
        nbdiffModelObj = nbdiffModel.query.filter(
            nbdiffModel.id == filename
        ).first()

        # bitarray used to convert BlOB to notebook data.
        notebook = bitarray.bitarray(nbdiffModelObj.notebook).tostring()
        return notebook


def newInstance():
    return NotebookRequestCommand()
