from . import BaseCommand
from flask import render_template, request

class FaqCommand(BaseCommand):

  def process(self, request, filename):
    return render_template('faq.html')
    
def newInstance():
  return FaqCommand()