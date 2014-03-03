from . import BaseCommand
from flask import send_from_directory, request
import os
import tempfile

class NotebookRequestCommand(BaseCommand):

  def process(self, request, filename):
    filepath = os.path.join(tempfile.gettempdir(), filename)
    file = open(filepath)
    notebook = file.read()
    file.close()
    #remove the tempfile in order to relieve server resource.
    os.remove(filepath)
    return notebook
    
def newInstance():
  return NotebookRequestCommand()