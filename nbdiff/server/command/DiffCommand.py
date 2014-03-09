from . import BaseCommand
from flask import render_template
from ...notebook_parser import NotebookParser
from ...notebook_diff import notebook_diff
import ntpath
import json
import tempfile


class DiffCommand(BaseCommand):

    def process(self, request, filename):
        before = request.form['beforeJSON']
        after = request.form['afterJSON']

        parser = NotebookParser()

        nb_before = parser.parseString(before)
        nb_after = parser.parseString(after)
        diffNotebook = notebook_diff(nb_before, nb_after)

        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(json.dumps(diffNotebook, indent=2))
        temp.close()

        nb_id = ntpath.basename(temp.name)

        return render_template(
            'nbdiff.html',
            project='/',
            base_project_url='/',
            base_kernel_url='/',
            notebook_id=nb_id,
            local=False
        )


def newInstance():
    return DiffCommand()
