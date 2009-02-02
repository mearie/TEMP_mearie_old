"""Rendering context.
"""

from __future__ import absolute_import, division, with_statement

from . import __version__
from .util import odict
from .http import HttpError

import httplib
import os.path

class Context(object):
    generator = 'mearieflo ' + __version__

    def __init__(self, app, environ):
        self.app = app
        self.path = None
        self.trail = ''
        self.status = httplib.OK
        self.headers = odict()
        self.environ = environ
        self.prefered_lang = None
        self.content_type = None
        self.content_enc = None

    def as_file(self):
        path = os.path.join(self.app.base, self.path)
        return open(path, 'r')

    def flush(self):
        pass # TODO

    @property
    def header_line(self):
        return '%d %s' % (self.status, httplib.responses[self.status])

    def perm_redirect(self, url):
        self.status = httplib.MOVED_PERMANENTLY
        self.headers['Location'] = url
        raise HttpError(self.status)

    def temp_redirect(self, url):
        self.status = httplib.TEMPORARY_REDIRECT
        self.headers['Location'] = url
        raise HttpError(self.status)

    def unauthorized(self):
        self.status = httplib.UNAUTHORIZED
        raise HttpError(self.status)

    def forbidden(self):
        self.status = httplib.FORBIDDEN
        raise HttpError(self.status)

    def not_found(self):
        self.status = httplib.NOT_FOUND
        raise HttpError(self.status)

    def not_acceptable(self):
        self.status = httplib.NOT_ACCEPTABLE
        raise HttpError(self.status)

    def gone(self):
        self.status = httplib.GONE
        raise HttpError(self.status)

    def internal_error(self):
        self.status = httplib.INTERNAL_SERVER_ERROR
        raise HttpError(self.status)

