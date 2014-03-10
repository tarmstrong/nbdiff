from . import BaseCommand
from flask import redirect
from ...notebook_parser import NotebookParser
from ...notebook_diff import notebook_diff
from nbdiff.server.database.nbdiffModel import nbdiffModel
import json
import bitarray


class DiffCommand(BaseCommand):

    def process(self, request, filename, db_session):
        before = request.form['beforeJSON']
        after = request.form['afterJSON']

        parser = NotebookParser()

        nb_before = parser.parseString(before)
        nb_after = parser.parseString(after)
        diffNotebook = notebook_diff(nb_before, nb_after)

        #bitarray used to convert notebook to binary for BLOB
        ba = bitarray.bitarray()
        ba.fromstring(json.dumps(diffNotebook, indent=2))
        
        #object to be saved to database
        obj = nbdiffModel(ba.to01())
        
        #add to database and commit it.
        db_session.add(obj)
        db_session.commit()
        
        #return the id of the object.
        nb_id = obj.id 
        
        #redirect is used because we want user to have a easier url to return to.
        return redirect("/Comparison/"+str(nb_id), code=302)


def newInstance():
    return DiffCommand()
