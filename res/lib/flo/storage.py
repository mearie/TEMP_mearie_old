"""Storage backend of mearieflo. This backend is used both for pages and for
metadata."""

from __future__ import absolute_import, division, with_statement

from .util import namedtuple

import os
import os.path


FileInfo = namedtuple('size')

class FileStorage(object):
    def __init__(self, base):
        self.base = base

    def open(self, path, mode='r'):
        path = os.path.join(self.base, path)
        return open(path, mode + 'b')

    def read(self, path):
        return self.open(path, 'r').read()

    def write(self, path, data):
        return self.open(path, 'w').

    def list(self, dirpath):
        path = os.path.join(self.base, path)
        return os.listdir(path)

    def info(self, path):
        path = os.path.join(self.base, path)
        stat = os.stat(path)
        return FileInfo(size=stat.st_size)

