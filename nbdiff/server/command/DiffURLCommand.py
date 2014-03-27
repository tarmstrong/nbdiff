from . import BaseCommand
from flask import redirect, render_template
from ...notebook_parser import NotebookParser
from ...notebook_diff import notebook_diff
from nbdiff.server.database.nbdiffModel import nbdiffModel
from werkzeug.exceptions import BadRequestKeyError
from sqlalchemy.exc import OperationalError
import urllib2
import json
import bitarray
import IPython.nbformat.current as nbformat


class DiffURLCommand(BaseCommand):

    def process(self, request, filename, db_session):
        errMsg = ""
        parser = NotebookParser()
        # Max Size of a notebook accepted is 20M.
        max_size = 20*1024*1024

        try:
            beforeURL = request.form['beforeURL']
            afterURL = request.form['afterURL']
        except BadRequestKeyError:
            errMsg = """Invalid notebook Diff Request. <br/>
                Please return to the home page and submit the request again."""
            return render_template('Error.html', err=errMsg)

        try:
            beforeFile = urllib2.urlopen(beforeURL)
            if int(beforeFile.info()['Content-Length']) > max_size:
                errMsg = errMsg + """The Before notebook exceeds 20MB.
                    Only notebooks below 20MB are accepted.<br/>"""
        except:
            errMsg = errMsg + """We are unable to access the Before
                notebook file from the given URL.<br/>"""

        try:
            afterFile = urllib2.urlopen(afterURL)
            if int(afterFile.info()['Content-Length']) > max_size:
                errMsg = errMsg + """The After notebook exceeds 20MB.
                    Only notebooks below 20MB are accepted.<br/>"""
        except:
            errMsg = errMsg + """We are unable to access the After
                notebook file from the given URL.<br/>"""

        if len(errMsg) == 0:
            try:
                nb_before = parser.parse(beforeFile)
            except nbformat.NotJSONError:
                errMsg = errMsg + """The Before notebook contains
                    invalid JSON data. <br/>"""
            try:
                nb_after = parser.parse(afterFile)
            except nbformat.NotJSONError:
                errMsg = errMsg + """The After notebook contains
                    invalid JSON data. <br/>"""

            beforeFile.close()
            afterFile.close()

        if len(errMsg) == 0:
            diffedNotebook = notebook_diff(nb_before, nb_after)

            # bitarray used to convert notebook to binary for BLOB
            ba = bitarray.bitarray()
            ba.fromstring(json.dumps(diffedNotebook, indent=2))

            # object to be saved to database
            obj = nbdiffModel(ba.to01())

            # add to database and commit it.
            try:
                db_session.add(obj)
                db_session.commit()
            except OperationalError:
                db_session.rollback()
                print """The database is not initialized.
                    Please restart server with argument init_db."""
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

            # redirect is used because we want
            # user to have a easier url to return to.
            return redirect("/Comparison/"+str(nb_id), code=302)
        else:
            return render_template('Error.html', err=errMsg)


def newInstance():
    return DiffURLCommand()
