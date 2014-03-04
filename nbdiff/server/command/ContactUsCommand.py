from . import BaseCommand
from flask import render_template, request

class ContactUsCommand(BaseCommand):

  def process(self, request, filename):
    return render_template('contactUs.html')
    
def newInstance():
  return ContactUsCommand()