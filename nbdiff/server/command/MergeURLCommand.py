from . import BaseCommand
from flask import redirect, render_template
from ...notebook_parser import NotebookParser
from ...merge import notebook_merge
from nbdiff.server.database.nbdiffModel import nbdiffModel
from werkzeug.exceptions import BadRequestKeyError
from sqlalchemy.exc import OperationalError
import urllib2
import json
import bitarray
import IPython.nbformat.current as nbformat


class MergeURLCommand(BaseCommand):

    def process(self, request, filename, db_session):
        errMsg = ""
        parser = NotebookParser()
        # Max Size of a notebook accepted is 20M.
        max_size = 20*1024*1024

        try:
            localURL = request.form['localURL']
            baseURL = request.form['baseURL']
            remoteURL = request.form['remoteURL']
        except BadRequestKeyError:
            errMsg = """Invalid notebook Merge Request.
                <br/>Please return to the home page and
                submit the request again."""
            return render_template('Error.html', err=errMsg)

        try:
            localFile = urllib2.urlopen(localURL)
            if int(localFile.info()['Content-Length']) > max_size:
                errMsg = errMsg + """The Local notebook
                    exceeds 20MB. Only notebooks below
                    20MB are accepted.<br/>"""
        except:
            errMsg = errMsg + """We are unable to access
                the Local notebook file from the
                given URL.<br/>"""

        try:
            baseFile = urllib2.urlopen(baseURL)
            if int(baseFile.info()['Content-Length']) > max_size:
                errMsg = errMsg + """The Base notebook
                    exceeds 20MB. Only notebooks below
                    20MB are accepted.<br/>"""
        except:
            errMsg = errMsg + """We are unable to access
                the Base notebook file from the given
                URL.<br/>"""

        try:
            remoteFile = urllib2.urlopen(remoteURL)
            if int(remoteFile.info()['Content-Length']) > max_size:
                errMsg = errMsg + """The Remote notebook
                    exceeds 20MB. Only notebooks below
                    20MB are accepted.<br/>"""
        except:
            errMsg = errMsg + """We are unable to access
                the Remote notebook file from
                the given URL.<br/>"""

        if len(errMsg) == 0:
            try:
                nb_local = parser.parse(localFile)
            except nbformat.NotJSONError:
                errMsg = errMsg + """The Local notebook
                    contains invalid JSON data. <br/>"""
            try:
                nb_base = parser.parse(baseFile)
            except nbformat.NotJSONError:
                errMsg = errMsg + """The Base notebook
                    contains invalid JSON data. <br/>"""
            try:
                nb_remote = parser.parse(remoteFile)
            except nbformat.NotJSONError:
                errMsg = errMsg + """The Remote notebook
                    contains invalid JSON data. <br/>"""

            localFile.close()
            baseFile.close()
            remoteFile.close()

        if len(errMsg) == 0:
            mergedNotebook = notebook_merge(nb_local, nb_base, nb_remote)

            # bitarray used to convert notebook to binary for BLOB
            ba = bitarray.bitarray()
            ba.fromstring(json.dumps(mergedNotebook, indent=2))

            # object to be saved to database
            obj = nbdiffModel(ba.to01())

            # add to database and commit it.
            try:
                db_session.add(obj)
                db_session.commit()
            except OperationalError:
                db_session.rollback()
                print """The database is not initialized.
                    Please restart server with argument init_db"""
                errMsg = """There was an error with the database. <br/>
                   Please contact administrator to resolve this issue."""
                return render_template('Error.html', err=errMsg)
            except:
                db_session.rollback()
                errMsg = """There was an unexpected error with the database.
                    <br/>Please try again later. <br/>
                    If this problem persists please contact administrator."""
                return render_template('Error.html', err=errMsg)

            # return the id of the object.
            nb_id = obj.id

            # redirect is used because we want users
            # to have a easier url to return to.
            return redirect("/Comparison/"+str(nb_id), code=302)
        else:
            return render_template('Error.html', err=errMsg)


def newInstance():
    return MergeURLCommand()
