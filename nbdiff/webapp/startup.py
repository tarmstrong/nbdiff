from flask import Flask, render_template
#, request
#import urllib2

app = Flask('NB Diff')


@app.route("/")
def upload():
    return render_template('upload.html')


@app.route("/merge", methods=['GET', 'POST'])
def merge():
    #local = request.form['localJSON']
    #remote = request.form['remoteJSON']
    #do magical comparison here /*
    comparedData = open("example-premerged-notebook.ipynb").read()
    return render_template('Merge.html', comparedData=comparedData)


@app.route("/mergeURL", methods=['GET', 'POST'])
def mergeURL():
    #https://www.dropbox.com/s/08n4aq6u6630iv1/left.ipynb
    #https://dl.dropboxusercontent.com/s/08n4aq6u6630iv1/left.ipynb
    #?dl=1&token_hash=AAGIQYzvIgsF1xvONTAtlhQK-kXPEcEIVgAgWLRnjAXInw
    #localURL = request.form['localURL']
    #localFile = urllib2.urlopen(localURL)
    #localJSON = localFile.read()
    #remoteURL = request.form['remoteURL']
    #remoteFile = urllib2.urlopen(remoteURL)
    #remoteJSON = remoteFile.read()
    #do magical comparison here /*
    comparedData = open("example-premerged-notebook.ipynb").read()
    return render_template('Merge.html', comparedData=comparedData)

if __name__ == "__main__":
    app.debug = True
    app.run()
