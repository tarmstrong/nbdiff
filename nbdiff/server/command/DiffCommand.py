from . import BaseCommand
from flask import redirect, render_template
from ...notebook_parser import NotebookParser
from ...notebook_diff import notebook_diff
from nbdiff.server.database.nbdiffModel import nbdiffModel
from werkzeug.exceptions import BadRequestKeyError
from sqlalchemy.exc import OperationalError
import json
import bitarray
import IPython.nbformat.current as nbformat


class DiffCommand(BaseCommand):

    def process(self, request, filename, db_session):
        errMsg = ""
        parser = NotebookParser()

        try:
            before = request.form['beforeJSON']
            after = request.form['afterJSON']
        except BadRequestKeyError:
            errMsg = """Invalid notebook Diff Request. <br/>
                Please return to the home page and submit the request again."""
            return render_template('Error.html', err=errMsg)

        try:
            nb_before = parser.parseString(before)
        except nbformat.NotJSONError:
            errMsg = errMsg + """The Before notebook contains
                invalid JSON data. <br/>"""
        try:
            nb_after = parser.parseString(after)
        except nbformat.NotJSONError:
            errMsg = errMsg + """The After notebook contains
                invalid JSON data. <br/>"""

        if len(errMsg) == 0:

            diffNotebook = notebook_diff(nb_before, nb_after)

            # bitarray used to convert notebook to binary for BLOB
            ba = bitarray.bitarray()
            ba.fromstring(json.dumps(diffNotebook, indent=2))

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

            # redirect is used because we want
            # user to have a easier url to return to.
            return redirect("/Comparison/"+str(nb_id), code=302)
        else:
            return render_template('Error.html', err=errMsg)


def newInstance():
    return DiffCommand()
