from . import BaseCommand
from flask import render_template
from nbdiff.server.database.nbdiffModel import nbdiffModel
from sqlalchemy.exc import OperationalError


class ComparisonCommand(BaseCommand):

    def process(self, request, filename, db_session):

        try:
            nbdiffModelObj = nbdiffModel.query.filter(
                nbdiffModel.id == filename
            ).first()
        except OperationalError:
            print """The database is not initialized.
                Please restart server with argument init_db"""
            errMsg = """There was an error with the database. <br/>
               Please contact administrator to resolve this issue."""
            return render_template('Error.html', err=errMsg)
        except:
            errMsg = """There was an unexpected error with the database. <br/>
                Please try again later. <br/>
                If this problem persists please contact administrator."""
            return render_template('Error.html', err=errMsg)

        # check that nbdiffModelObj exists before redirecting to nbdiff.html.
        # Either the Comparison does not exist or expired from server
        # and was dropped from Database.
        if nbdiffModelObj is None:
            errMsg = """The Merge or Diff is not available. <br/>
                Either the Merge or Diff expired or does not exist. <br/>
                Please return to the Home Page to
                request another comparison."""
            return render_template('Error.html', err=errMsg)
        else:
            return render_template(
                'nbdiff.html',
                project='/',
                base_project_url='/',
                base_kernel_url='/',
                notebook_id=filename,
                local=False
            )


def newInstance():
    return ComparisonCommand()
