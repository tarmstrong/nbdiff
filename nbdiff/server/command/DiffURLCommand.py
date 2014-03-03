from . import BaseCommand
from flask import render_template, request
from ...notebook_parser import NotebookParser
from ...notebook_diff import notebook_diff
import ntpath
import tempfile
import urllib2
import json

class DiffURLCommand(BaseCommand):

  def process(self, request, filename):

    #example url of a .ipynb
    #https://dl.dropboxusercontent.com/s/08n4aq6u6630iv1/before.ipynb?dl=1&token_hash=AAGIQYzvIgsF1xvONTAtlhQK-kXPEcEIVgAgWLRnjAXInw
    parser = NotebookParser()

    beforeURL = request.form['beforeURL']
    beforeFile = urllib2.urlopen(beforeURL)
    nb_before = parser.parse(beforeFile)
    beforeFile.close()

    afterURL = request.form['afterURL']
    afterFile = urllib2.urlopen(afterURL)
    nb_after = parser.parse(afterFile)
    afterFile.close()

    diffedNotebook = notebook_diff(nb_before, nb_after)
    print "a"
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(json.dumps(diffedNotebook, indent=2))
    temp.close()
    print "a"
    nb_id = ntpath.basename(temp.name)
    print "a"
    return render_template('nbdiff.html', project='/', base_project_url='/', base_kernel_url='/', notebook_id=nb_id, remote=True)
    
def newInstance():
  return DiffURLCommand()