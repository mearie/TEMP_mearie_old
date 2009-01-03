"""Rendering context.
"""

from __future__ import absolute_import, division, with_statement

from . import __version__

class Context(object):
    generator = 'mearieflo ' + __version__

    def __init__(self, trail=''):
        self.subpath = trail

    def flush(self):
        pass # TODO

