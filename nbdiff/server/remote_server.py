from flask import Flask, render_template, send_from_directory, request
import urllib2
import jinja2
import json
import IPython.html
import os
import sys
import tempfile
import ntpath

from ..merge import notebook_merge
from ..notebook_parser import NotebookParser


class NbFlask(Flask):
    jinja_loader = jinja2.FileSystemLoader([
        IPython.html.__path__[0] + '/templates',
        os.path.dirname(os.path.realpath(__file__)) + '/templates'
    ])

    notebooks = []

    def shutdown_callback(self, callback):
        self.shutdown = callback

    def add_notebook(self, nb):
        self.notebooks.append(nb)

app = NbFlask(__name__, static_folder=IPython.html.__path__[0] + '/static')

#used to define the directory for resources used in html pages. 
@app.route('/nbdiff/<path:filename>')
def nbdiff_static(filename):
    return send_from_directory(os.path.dirname(os.path.realpath(__file__))
                               + '/static', filename)

@app.route("/")
def upload():
    return render_template('upload.html')


@app.route("/merge", methods=['GET', 'POST'])
def merge():
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

    return render_template('nbdiff.html', project='/', base_project_url='/', base_kernel_url='/', notebook_id=nb_id)


@app.route("/mergeURL", methods=['GET', 'POST'])
def mergeURL():

    #example url of a .ipynb
    #https://dl.dropboxusercontent.com/s/08n4aq6u6630iv1/left.ipynb
    #?dl=1&token_hash=AAGIQYzvIgsF1xvONTAtlhQK-kXPEcEIVgAgWLRnjAXInw
    localURL = request.form['localURL']
    localFile = urllib2.urlopen(localURL)

    baseURL = request.form['baseURL']
    baseFile = urllib2.urlopen(baseURL)

    remoteURL = request.form['remoteURL']
    remoteFile = urllib2.urlopen(remoteURL)

    parser = NotebookParser()

    nb_local = parser.parseString(localFile)
    nb_base = parser.parseString(baseFile)
    nb_remote = parser.parseString(remoteFile)
    mergedNotebook = notebook_merge(nb_local, nb_base, nb_remote)

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(json.dumps(mergedNotebook, indent=2))
    temp.close()

    nb_id = ntpath.basename(temp.name)

    return render_template('nbdiff.html', project='/', base_project_url='/', base_kernel_url='/', notebook_id=nb_id)

@app.route('/notebooks/<path:path>', methods=['GET', 'PUT'])
def notebookRequest(path):
    if request.method == 'PUT':
        app.shutdown(request.data)
        request.environ.get('werkzeug.server.shutdown')()
        return ""
    else:
        filepath = os.path.join(tempfile.gettempdir(), path)
        file = open(filepath)
        notebook = file.read()
        file.close()
        #remove the tempfile in order to relieve server resource.
        os.remove(filepath)
        return notebook

if __name__ == "__main__":
    app.debug = False
    app.run()
