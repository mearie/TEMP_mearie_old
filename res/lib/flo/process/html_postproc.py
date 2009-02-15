"""HTML postprocessor, converts various pseudo-HTML tags to valid HTML.
"""

from __future__ import absolute_import, division, with_statement

from xml.dom.minidom import parse, parseString
import os

# This internal type should not be final media type!
_HTMLTREETYPE = 'application/prs.mearieflo.xml-dom-tree'

class HTMLTreeReader(object):
    """Parses pseudo-(X)HTML to DOM tree. It returns the internal media type
    and should be followed by HTMLTreeWriter later."""

    input_type = ['text/html', 'application/xhtml+xml']
    output_type = _HTMLTREETYPE

    def __init__(self, base):
        self.base = base

    def __call__(self, context, data):
        if data is None:
            return parse(context.as_path())
        else:
            return parseString(data)

class HTMLTreeWriter(object):
    """Converts DOM tree to (X)HTML back."""

    input_type = [_HTMLTREETYPE]
    output_type = 'text/html'

    def __call__(self, context, xml):
        assert xml is not None

        try:
            return xml.toxml(encoding='utf-8')
        finally:
            xml.unlink()

class ReferencesInserter(object):
    """Processes ref/fn and references/footnotes pseudo-element to actual
    (X)HTML. The former introduces a link to actual footnote, and the latter
    prints all previous footnotes into container.
    
    Input format should be DOM tree."""

    input_type = [_HTMLTREETYPE]
    output_type = _HTMLTREETYPE

    def __call__(self, context, xml):
        assert xml is not None

        references = []

        def process_ref(xml, el, nextnum, references=references):
            refname = el.getAttribute('name')
            if not refname:
                refname = str(nextnum)
                nextnum += 1
            if el.hasChildNodes():
                references.append((refname, el))

            reflink = xml.createElement('a')
            reflink.setAttribute('class', 'ref-link')
            reflink.setAttribute('href', '#ref:' + refname)
            reflink.appendChild(xml.createTextNode('[' + refname + ']'))
            el.parentNode.replaceChild(reflink, el)

            nextnum = process(xml, el, nextnum)
            return nextnum

        def process_reflist(xml, el, nextnum, references=references):
            nextnum = process(xml, el, nextnum)

            if references:
                refs = xml.createElement('div')
                refs.setAttribute('class', 'references')
                for refname, refel in references:
                    ref = xml.createElement('div')
                    ref.setAttribute('class', 'reference')
                    ref.setAttribute('id', 'ref:' + refname)
                    refnum = xml.createElement('span')
                    refnum.setAttribute('class', 'ref-label')
                    refnum.appendChild(xml.createTextNode('[' + refname + '] '))
                    ref.appendChild(refnum)
                    for child in refel.childNodes[:]:
                        ref.appendChild(child)
                    refs.appendChild(ref)
                el.parentNode.replaceChild(refs, el)
            else:
                el.parentNode.removeChild(el)

            del references[:]
            return nextnum

        def process(xml, el, nextnum, references=references):
            for child in el.childNodes:
                if child.nodeType == 1: # ELEMENT_NODE
                    if child.tagName in ('ref', 'fn'):
                        nextnum = process_ref(xml, child, nextnum)
                    elif child.tagName in ('references', 'footnotes'):
                        nextnum = process_reflist(xml, child, nextnum)
                    else:
                        nextnum = process(xml, child, nextnum)

            return nextnum

        process(xml, xml, 1)
        return xml

class MathReplacer(object):
    """Processes m pseudo-element to actual (X)HTML. m pseudo-element should
    contain valid LaTeX equation, as if contained in $...$ block. It prints
    placeholder span element to be converted in the client side.

    Input format should be DOM tree."""

    input_type = [_HTMLTREETYPE]
    output_type = _HTMLTREETYPE

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

class ImageFramer(object):
    """Processes non-singleton img element to valid (X)HTML. When img element
    has child nodes it is interpreted to the image's description (as like
    XHTML2) and converted to container and actual image.

    Input format should be DOM tree. If img doesn't have correct width attribute,
    it should be filled before this processor."""

    input_type = [_HTMLTREETYPE]
    output_type = _HTMLTREETYPE

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

class AbbreviationFiller(object):
    """Fills title attribute of abbr element if none. It reads predefined
    acronyms from .flo/acronyms.conf which contains acronym and description
    separated by whitespaces first.

    .flo/acronyms.conf can contain a comment line starting with # or ;.
    If multiple acronym.conf are present, inner line takes precedence.

    Input format should be DOM tree."""

    input_type = [_HTMLTREETYPE]
    output_type = _HTMLTREETYPE

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

