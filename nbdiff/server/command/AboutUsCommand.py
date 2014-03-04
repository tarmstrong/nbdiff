from . import BaseCommand
from flask import render_template, request

class AboutUsCommand(BaseCommand):

  def process(self, request, filename):
    return render_template('aboutUs.html')
    
def newInstance():
  return AboutUsCommand()