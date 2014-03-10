from . import BaseCommand
from flask import redirect
from ...notebook_parser import NotebookParser
from ...notebook_diff import notebook_diff
from nbdiff.server.database.nbdiffModel import nbdiffModel
import urllib2
import json
import bitarray


class DiffURLCommand(BaseCommand):

    def process(self, request, filename, db_session):
        parser = NotebookParser()

        beforeURL = request.form['beforeURL']
        beforeFile = urllib2.urlopen(beforeURL)
        nb_before = parser.parse(beforeFile)
        beforeFile.close()

        afterURL = request.form['afterURL']
        afterFile = urllib2.urlopen(afterURL)
        nb_after = parser.parse(afterFile)
        afterFile.close()

        diffedNotebook = notebook_diff(nb_before, nb_after)
        
        #bitarray used to convert notebook to binary for BLOB
        ba = bitarray.bitarray()
        ba.fromstring(json.dumps(diffedNotebook, indent=2))
        
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
    return DiffURLCommand()
