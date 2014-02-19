from flask import Flask, render_template, send_from_directory, request
import urllib2
import jinja2
import json
import IPython.html
import os
import sys


execfile("C:\\Users\\Azn0Richard0\\Documents\\GitHub\\nbdiff\\nbdiff\\merge.py")


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

@app.route("/")
def upload():
    return render_template('upload.html')


@app.route("/merge", methods=['GET', 'POST'])
def merge():
    local = request.form['localJSON']
    remote = request.form['remoteJSON']
    base = request.form['baseJSON']
    #do magical comparison here /*
    comparedData = open("example-premerged-notebook.ipynb").read()
    return render_template('Merge.html', comparedData=comparedData)


@app.route("/mergeURL", methods=['GET', 'POST'])
def mergeURL():
    
    #example url of a .ipynb
    #https://dl.dropboxusercontent.com/s/08n4aq6u6630iv1/left.ipynb
    #?dl=1&token_hash=AAGIQYzvIgsF1xvONTAtlhQK-kXPEcEIVgAgWLRnjAXInw
    localURL = request.form['localURL']
    localFile = urllib2.urlopen(localURL)
    localJSON = localFile.read()
    
    baseURL = request.form['baseURL']
    baseFile = urllib2.urlopen(baseURL)
    baseJSON = baseFile.read()
    
    remoteURL = request.form['remoteURL']
    remoteFile = urllib2.urlopen(remoteURL)
    remoteJSON = remoteFile.read()
    
    #do magical comparison here /*
    comparedData = open("example-premerged-notebook.ipynb").read()
    return render_template('Merge.html', comparedData=comparedData)
    

if __name__ == "__main__":
    app.debug = True
    app.run()
