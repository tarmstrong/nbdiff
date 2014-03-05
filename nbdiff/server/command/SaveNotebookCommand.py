from . import BaseCommand
from flask import render_template, request, make_response
from IPython.nbformat import current
from unicodedata import normalize

import tempfile
import ntpath
import json

class SaveNotebookCommand(BaseCommand):

  def process(self, request, filename):
    #format for notebook. 
    format = u'json'
    data =  request.form['download_data']
    
    try:
        #read notebook and format it. 
        nb = current.reads(data.decode('utf-8'), format)
    except:
        return "Unable to save notebook. Invalid JSON data"
    
    #if notebook has a name we use it else use a generic name
    try:
        name = nb.metadata.name
    except:
        name = "mergedNotebook"
        nb.metadata.name = name
    
    name = normalize('NFC', nb.metadata.name)  
    
    #uses ipython's current ipynb formatting.
    notebook_formatted = current.writes(nb, format)
    
    #make a file download response 
    response = make_response(notebook_formatted)
    response.headers["Content-Disposition"] = "attachment; filename="+name+".ipynb"
    
    return response
    
def newInstance():
  return SaveNotebookCommand()