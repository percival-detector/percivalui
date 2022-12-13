"""
Created on 1 August 2017

@author: Alan Greer
"""
import os
from logging.handlers import RotatingFileHandler


class MkDirRotatingFileHandler(RotatingFileHandler):
    """
    Subclass of RotatingFileHandler that attempts to create any directories required by the log file.
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        #self._clean_directory(filename)
        RotatingFileHandler.__init__(self, filename, mode, maxBytes, backupCount, encoding, delay)

    #def _clean_directory(self, filename):
    #    file = os.path.basename(filename)
    #    directory = os.path.dirname(filename)
    #    for the_file in os.listdir(directory):
    #        if file in the_file:
    #            file_path = os.path.join(directory, the_file)
    #            try:
    #                if os.path.isfile(file_path):
    #                    os.unlink(file_path)
    #            except Exception as e:
    #                print(e)
