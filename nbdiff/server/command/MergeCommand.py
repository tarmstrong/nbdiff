from . import BaseCommand
from flask import render_template, request
from ...notebook_parser import NotebookParser
from ...merge import notebook_merge
import ntpath
import json
import tempfile

class MergeCommand(BaseCommand):

  def process(self, request, filename):
    local = request.form['localJSON']
    remote = request.form['remoteJSON']
    base = request.form['baseJSON']

    parser = NotebookParser()

    nb_local = parser.parseString(local)
    nb_base = parser.parseString(base)
    nb_remote = parser.parseString(remote)
    mergedNotebook = notebook_merge(nb_local, nb_base, nb_remote)

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(json.dumps(mergedNotebook, indent=2))
    temp.close()

    nb_id = ntpath.basename(temp.name)

    return render_template('nbdiff.html', project='/', base_project_url='/', base_kernel_url='/', notebook_id=nb_id, remote=True)
    
def newInstance():
  return MergeCommand()