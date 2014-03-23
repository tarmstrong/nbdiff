from . import BaseCommand
from flask import send_from_directory
import os


class ResourceRequestCommand(BaseCommand):

    def process(self, request, filename, db_session):
        return send_from_directory(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..")
            ) + '/static',
            filename
        )


def newInstance():
    return ResourceRequestCommand()
