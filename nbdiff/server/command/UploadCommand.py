from . import BaseCommand
from flask import render_template


class UploadCommand(BaseCommand):

    def process(self, request, filename):
        return render_template('upload.html')


def newInstance():
    return UploadCommand()
