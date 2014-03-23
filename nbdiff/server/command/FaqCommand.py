from . import BaseCommand
from flask import render_template


class FaqCommand(BaseCommand):

    def process(self, request, filename, db_session):
        return render_template('faq.html')


def newInstance():
        return FaqCommand()
