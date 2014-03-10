from . import BaseCommand
from flask import render_template


class AboutUsCommand(BaseCommand):

    def process(self, request, filename, db_session):
        return render_template('aboutUs.html')


def newInstance():
    return AboutUsCommand()
