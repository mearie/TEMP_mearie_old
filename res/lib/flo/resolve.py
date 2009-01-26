"""Path resolver.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context

from mako.lookup import TemplateLookup

import os, os.path

class Resolver(object):
    def __init__(self, base):
        self.base = os.path.normpath(base)

    def canonicalize(self, path):
        path = os.path.normpath(path.lstrip('/'))
        if path.startswith('..'): path = ''
        return os.path.join(self.base, path)

    def resolve(self, app, environ):
        context = Context(app, environ)

        context.path = path = environ['PATH_INFO']
        assert path.startswith('/')

        scriptbase = self.base
        if not os.path.isdir(scriptbase):
            context.not_found()

        pos = 0
        while pos < len(path):
            npos = path.find('/', pos+1)
            if npos < 0: npos = len(path)
            component = path[pos+1:npos]
            pos = npos
            if component:
                if component == '..':
                    newbase = os.path.split(scriptbase)[0]
                else:
                    newbase = os.path.join(scriptbase, component)
                if not newbase.startswith(self.base):
                    context.not_found()
                if not os.path.isdir(newbase): break
                scriptbase = newbase
        else:
            component = 'index' # default filename
            if not path.endswith('/'):
                context.perm_redirect(path + '/')

        assert os.path.isdir(scriptbase)
        prefix = component + '.'
        trail = path[pos:]

        for name in os.listdir(scriptbase):
            fullname = os.path.join(scriptbase, name)
            if not os.path.isfile(fullname): continue
            if name == component or name.startswith(prefix):
                # TODO negotiation
                context.path = fullname
                context.trail = trail
                return context

        context.not_found()

