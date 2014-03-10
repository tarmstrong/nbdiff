from . import BaseCommand
from flask import render_template


class ComparisonCommand(BaseCommand):

    def process(self, request, filename, db_session):
    
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