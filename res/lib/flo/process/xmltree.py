"""Intermediate processor for XML DOM tree input and output.
"""

from __future__ import absolute_import, division, with_statement

from xml.dom.minidom import parse, parseString

# should not be final type.
XMLTREETYPE = 'application/prs.mearieflo.xml-dom-tree'

class XMLTreeReader(object):
    """Parses pseudo-(X)HTML to XML tree. It returns the internal media type
    and should be followed by HTMLTreeWriter later."""

    input_type = ['text/html', 'application/xhtml+xml']
    output_type = XMLTREETYPE

    def __init__(self, base):
        self.base = base

    def __call__(self, context, data):
        if data is None:
            return parse(context.as_path())
        else:
            return parseString(data)

class XMLTreeWriter(object):
    """Converts XML tree to (X)HTML back."""

    input_type = [XMLTREETYPE]
    output_type = 'text/html'

    def __call__(self, context, xml):
        assert xml is not None

        try:
            data = xml.toxml().encode('utf-8')
            assert data.startswith('<?xml version="1.0" ?>')
            return data[22:]
        finally:
            xml.unlink()

