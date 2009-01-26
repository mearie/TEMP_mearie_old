"""Rendering context.
"""

from __future__ import absolute_import, division, with_statement

from . import __version__
from .util import odict

import httplib

class HttpError(Exception):
    def __init__(self, status, context):
        Exception.__init__(self, status, context)
        context.status = status

    def __repr__(self):
        status, context = self.args
        return '%s(httplib.%s, %r)' % (self.__class__.__name__,
                httplib.responses[status].upper().replace(' ','_').replace('-','_'),
                context)

class Context(object):
    generator = 'mearieflo ' + __version__

    def __init__(self, app, environ):
        self.app = app
        self.path = None
        self.trail = ''
        self.status = httplib.OK
        self.headers = odict()
        self.environ = environ

    def flush(self):
        pass # TODO

    @property
    def header_line(self):
        return '%d %s' % (self.status, httplib.responses[self.status])

    def perm_redirect(self, url):
        self.headers['Location'] = url
        raise HttpError(httplib.MOVED_PERMANENTLY, self)

    def temp_redirect(self, url):
        self.headers['Location'] = url
        raise HttpError(httplib.TEMPORARY_REDIRECT, self)

    def not_found(self):
        raise HttpError(httplib.NOT_FOUND, self)

    def forbidden(self):
        raise HttpError(httplib.FORBIDDEN, self)

    def gone(self):
        raise HttpError(httplib.GONE, self)

    def internal_error(self):
        raise HttpError(httplib.INTERNAL_SERVER_ERROR, self)

