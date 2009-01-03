"""Rendering context.
"""

from __future__ import absolute_import, division, with_statement

from mako.runtime import Context as ContextBase

class Context(ContextBase):
    def __init__(self, buffer, data={}, **kwargs):
        ContextBase.__init__(self, buffer, **data)
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def flush(self):
        pass # TODO

