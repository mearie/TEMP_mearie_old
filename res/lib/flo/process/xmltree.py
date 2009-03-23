"""Intermediate processor for XML DOM tree input and output.
"""

from __future__ import absolute_import, division, with_statement

from xml.dom.minidom import parse, parseString

# should not be final type.
_TREETYPE_HTML = 'application/prs.mearieflo.xml-tree.html'
_TREETYPE_XHTML = 'application/prs.mearieflo.xml-tree.xhtml'

class XMLTreeReader(object):
    """Parses pseudo-(X)HTML to XML tree. It returns the internal media type
    and should be followed by HTMLTreeWriter later."""

    def accepts(self, context, type):
        if type == 'text/html':
            return _TREETYPE_HTML
        if type == 'application/xhtml+xml':
            return _TREETYPE_XHTML
        return None

    def __call__(self, context, data):
        if data is None:
            return parse(context.as_path())
        else:
            return parseString(data)

class XMLTreeWriter(object):
    """Converts XML tree to (X)HTML back."""

    def accepts(self, context, type):
        if type == _TREETYPE_HTML:
            return 'text/html'
        if type == _TREETYPE_XHTML:
            return 'application/xhtml+xml'
        return None

    def __call__(self, context, xml):
        assert xml is not None

        try:
            data = xml.toxml().encode('utf-8')
            assert data.startswith('<?xml version="1.0" ?>')
            return data[22:]
        finally:
            xml.unlink()

class XMLTreeProcessor(object):
    """Superclass of processors excepting XML tree. It implements accepts
    method."""

    def accepts(self, context, type):
        if type == _TREETYPE_HTML or type == _TREETYPE_XHTML:
            return type
        return None

