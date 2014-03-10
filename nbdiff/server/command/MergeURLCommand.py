from . import BaseCommand
from flask import redirect
from ...notebook_parser import NotebookParser
from ...merge import notebook_merge
from nbdiff.server.database.nbdiffModel import nbdiffModel
import urllib2
import json
import bitarray


class MergeURLCommand(BaseCommand):

    def process(self, request, filename, db_session):
        parser = NotebookParser()

        localURL = request.form['localURL']
        localFile = urllib2.urlopen(localURL)
        nb_local = parser.parse(localFile)
        localFile.close()

        baseURL = request.form['baseURL']
        baseFile = urllib2.urlopen(baseURL)
        nb_base = parser.parse(baseFile)
        baseFile.close()

        remoteURL = request.form['remoteURL']
        remoteFile = urllib2.urlopen(remoteURL)
        nb_remote = parser.parse(remoteFile)
        remoteFile.close()

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
    return MergeURLCommand()
