"""HTML sanitizing processor.
"""

from __future__ import absolute_import, division, with_statement

from xml.dom.minidom import parse, parseString

class HTMLSanitizer(object):
    input_type = ['text/html', 'application/xhtml+xml']
    output_type = 'text/html'

    def __init__(self, base):
        self.base = base

    def __call__(self, context, data):
        if data is None:
            path = os.path.join(self.base, context.path)
            xml = parse(open(path, 'r'))
        else:
            xml = parseString(data)

        try:
            for el in xml.getElementsByTagName('foo'):
                newel = xml.createElement('p')
                newel.appendChild(xml.createTextNode('FOO!'))
                el.parentNode.replaceChild(newel, el)

            return xml.toxml(encoding='utf-8')
        finally:
            xml.unlink()

