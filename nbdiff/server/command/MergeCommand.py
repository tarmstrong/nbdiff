from . import BaseCommand
from flask import redirect
from ...notebook_parser import NotebookParser
from ...merge import notebook_merge
from nbdiff.server.database.nbdiffModel import nbdiffModel
import json
import bitarray

class MergeCommand(BaseCommand):

    def process(self, request, filename, db_session):
    
        local = request.form['localJSON']
        remote = request.form['remoteJSON']
        base = request.form['baseJSON']

        parser = NotebookParser()

        nb_local = parser.parseString(local)
        nb_base = parser.parseString(base)
        nb_remote = parser.parseString(remote)
        mergedNotebook = notebook_merge(nb_local, nb_base, nb_remote)
           
        #bitarray used to convert notebook to binary for BLOB
        ba = bitarray.bitarray()
        ba.fromstring(json.dumps(mergedNotebook, indent=2))
        
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
    return MergeCommand()
