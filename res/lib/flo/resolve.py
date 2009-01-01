"""Path resolver.
"""

from __future__ import absolute_import, division, with_statement

from mako.lookup import TemplateLookup

import os, os.path

class Resolver(object):
    def __init__(self, base):
        self.base = base

    def canonicalize(self, path):
        path = os.path.normpath(path.lstrip('/'))
        if path.startswith('..'): path = ''
        return os.path.join(self.base, path)

    def resolve(self, path):
        path = self.canonicalize(path)
        if os.path.isdir(path):
            path = os.path.join(path, 'index')
        if os.path.splitext(path)[1] == '':
            path += '.html'

        if not os.path.exists(path): return None
        return path

