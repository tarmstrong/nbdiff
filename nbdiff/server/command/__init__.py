#abstract base class
from abc import ABCMeta, abstractmethod
from flask import request

class BaseCommand(object):
  __metaclass__ = ABCMeta
    
  @abstractmethod
  def process(self, request, filename):
    pass