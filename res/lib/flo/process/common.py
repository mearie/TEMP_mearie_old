"""Common implementation of processor.
"""

from __future__ import absolute_import, division, with_statement

class BaseProcessor(object):
    def __init__(self, app):
        pass # app object is not used.

    def accepts(self, context, type):
        raise NotImplemented

    def __call__(self, context, data):
        raise NotImplemented

class BaseHTMLProcessor(BaseProcessor):
    def accepts(self, context, type):
        if type == 'text/html' or type == 'application/xhtml+xml':
            return type
        return None

