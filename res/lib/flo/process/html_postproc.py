"""HTML postprocessor, converts various pseudo-HTML tags to valid HTML.
"""

from __future__ import absolute_import, division, with_statement

from .xmltree import XMLTreeProcessor

class MathReplacer(XMLTreeProcessor):
    """Processes m pseudo-element to actual (X)HTML. m pseudo-element should
    contain valid LaTeX equation, as if contained in $...$ block. It prints
    placeholder span element to be converted in the client side.

    Input format should be XML tree."""

    def __call__(self, context, xml):
        assert xml is not None

        for el in xml.getElementsByTagName('m'):
            size = 1
            try:
                size += int(el.getAttribute('size'))
                if size < -4: size = -4
                if size > +4: size = +4
            except:
                pass

            span = xml.createElement('span')
            el.parentNode.replaceChild(span, el)
            span.setAttribute('class', 'math math-size%d' % size)
            for child in el.childNodes[:]:
                el.removeChild(child)
                span.appendChild(child)

        return xml

class ImageFramer(XMLTreeProcessor):
    """Processes non-singleton img element to valid (X)HTML. When img element
    has child nodes it is interpreted to the image's description (as like
    XHTML2) and converted to container and actual image.

    Input format should be XML tree. If img doesn't have correct width attribute,
    it should be filled before this processor."""

    def __call__(self, context, xml):
        assert xml is not None

        for el in xml.getElementsByTagName('img'):
            if not el.hasChildNodes(): continue
            frame = xml.createElement('div')
            el.parentNode.replaceChild(frame, el)
            frame.setAttribute('class', 'image-frame ' + el.getAttribute('class'))
            frame.setAttribute('style', 'width:%spx' % el.getAttribute('width'))
            el.removeAttribute('class')
            el.setAttribute('alt', '')
            frame.appendChild(el)
            frame.appendChild(xml.createTextNode(' '))
            for child in el.childNodes[:]:
                el.removeChild(child)
                frame.appendChild(child)

        return xml

class AbbreviationFiller(XMLTreeProcessor):
    """Fills title attribute of abbr element if none. It reads predefined
    acronyms from .flo/acronyms.conf which contains acronym and description
    separated by whitespaces first.

    .flo/acronyms.conf can contain a comment line starting with # or ;.
    If multiple acronym.conf are present, inner line takes precedence.

    Input format should be XML tree."""

    def read_acronyms(self, context):
        acronyms = {}
        for path in context.conf.paths('.flo', 'acronyms.conf'):
            try:
                for line in open(path, 'r'):
                    if line.startswith('#') or line.startswith(';'): continue
                    line = line.split(None, 1)
                    if len(line) == 2:
                        key = line[0].decode('utf-8').lower()
                        value = line[1].decode('utf-8').rstrip()
                        if key not in acronyms: acronyms[key] = value
            except: pass
        return acronyms

    def __call__(self, context, xml):
        assert xml is not None
        acronyms = None

        for el in xml.getElementsByTagName('abbr'):
            if el.getAttribute('title') == '':
                if acronyms is None:
                    acronyms = self.read_acronyms(context)
                text = el.childNodes[0].nodeValue
                el.setAttribute('title', acronyms.get(text.lower(), u''))

        return xml

