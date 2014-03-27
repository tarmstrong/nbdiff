# abstract base class
from abc import ABCMeta, abstractmethod


class BaseCommand(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, request, filename, db_session):
        pass
