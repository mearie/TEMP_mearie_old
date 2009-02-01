"""HTML sanitizing processor.
"""

from __future__ import absolute_import, division, with_statement

class HTMLSanitizer(object):
    input_type = ['text/html', 'application/xhtml+xml']
    output_type = 'text/html'

    def __init__(self, base):
        self.base = base

    def __call__(self, context, data):
        if data is None:
            data = open(os.path.join(self.base, context.path), 'r')

        return data.strip()

