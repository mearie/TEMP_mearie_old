"""Converts application/xhtml+xml media type to text/html for legacy browsers.
For convenience, it can also convert text/html media type to application/
xhtml+xml if supported.

(See http://hixie.ch/advocacy/xhtml for rationale behind not using text/html.)
"""

from __future__ import absolute_import, division, with_statement

class XHTMLTypeConverter(object):
    def __init__(self, convert_html=True):
        self.convert_html = convert_html

    def accepts(self, context, type):
        # detect explicit (not */*, like MSIE) intention for XHTML response.
        if context.accepts.match('application/xhtml+xml') and \
                'application/xhtml+xml' in context.environ.get('HTTP_ACCEPT', ''):
            if self.convert_html and type == 'text/html':
                return 'application/xhtml+xml'
        else:
            if type == 'application/xhtml+xml':
                return 'text/html'

        return None

    def __call__(self, context, data):
        return data

