from . import BaseCommand
from flask import redirect, render_template
from ...notebook_parser import NotebookParser
from ...merge import notebook_merge
from nbdiff.server.database.nbdiffModel import nbdiffModel
from werkzeug.exceptions import BadRequestKeyError
from sqlalchemy.exc import OperationalError
import json
import bitarray
import IPython.nbformat.current as nbformat


class MergeCommand(BaseCommand):

    def process(self, request, filename, db_session):

        errMsg = ""
        parser = NotebookParser()

        try:
            local = request.form['localJSON']
            remote = request.form['remoteJSON']
            base = request.form['baseJSON']
        except BadRequestKeyError:
            errMsg = """Invalid notebook Merge Request. <br/>
                Please return to the home page and submit the request again."""
            return render_template('Error.html', err=errMsg)

        try:
            nb_local = parser.parseString(local)
        except nbformat.NotJSONError:
            errMsg = errMsg + """The Local notebook contains
                invalid JSON data. <br/>"""
        try:
            nb_base = parser.parseString(base)
        except nbformat.NotJSONError:
            errMsg = errMsg + """The Base notebook contains
                invalid JSON data. <br/>"""
        try:
            nb_remote = parser.parseString(remote)
        except nbformat.NotJSONError:
            errMsg = errMsg + """The Remote notebook contains
                invalid JSON data. <br/>"""

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
                errMsg = """There was an unexpected error with
                    the database. <br/>Please try again later. <br/>
                    If this problem persists please contact administrator."""
                return render_template('Error.html', err=errMsg)

            # return the id of the object.
            nb_id = obj.id

            # redirect is used because we want user
            # to have a easier url to return to.
            return redirect("/Comparison/"+str(nb_id), code=302)
        else:
            return render_template('Error.html', err=errMsg)


def newInstance():
    return MergeCommand()
