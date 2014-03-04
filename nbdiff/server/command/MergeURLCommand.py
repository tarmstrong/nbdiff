from . import BaseCommand
from flask import render_template, request
from ...notebook_parser import NotebookParser
from ...merge import notebook_merge
import ntpath
import tempfile
import urllib2
import json

class MergeURLCommand(BaseCommand):

  def process(self, request, filename):
    #example url of a .ipynb
    #https://dl.dropboxusercontent.com/s/08n4aq6u6630iv1/left.ipynb?dl=1&token_hash=AAGIQYzvIgsF1xvONTAtlhQK-kXPEcEIVgAgWLRnjAXInw
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

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(json.dumps(mergedNotebook, indent=2))
    temp.close()

    nb_id = ntpath.basename(temp.name)

    return render_template('nbdiff.html', project='/', base_project_url='/', base_kernel_url='/', notebook_id=nb_id, local=False)
    
def newInstance():
  return MergeURLCommand()