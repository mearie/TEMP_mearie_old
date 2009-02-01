"""HTML postprocessor, converts various pseudo-HTML tags to valid HTML.
"""

from __future__ import absolute_import, division, with_statement

from xml.dom.minidom import parse, parseString

# This internal type should not be final media type!
_HTMLTREETYPE = 'application/prs.mearieflo.xml-dom-tree'

class HTMLTreeReader(object):
    input_type = ['text/html', 'application/xhtml+xml']
    output_type = _HTMLTREETYPE

    def __call__(self, context, data):
        if data is None:
            path = os.path.join(self.base, context.path)
            return parse(open(path, 'r'))
        else:
            return parseString(data)

class HTMLTreeWriter(object):
    input_type = [_HTMLTREETYPE]
    output_type = 'text/html'

    def __call__(self, context, xml):
        assert xml is not None

        try:
            return xml.toxml(encoding='utf-8')
        finally:
            xml.unlink()

class ReferencesInserter(object):
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
                references.append((refname, el.childNodes[:]))

            reflink = xml.createElement('a')
            reflink.setAttribute('class', 'ref-link')
            reflink.setAttribute('href', '#ref:' + refname)
            reflink.appendChild(xml.createTextNode('[' + refname + ']'))
            el.parentNode.replaceChild(reflink, el)

            nextnum = process(xml, el, nextnum)
            return nextnum

        def process_reflist(xml, el, nextnum, references=references):
            nextnum = process(xml, el, nextnum)
            if not references: return

            refs = xml.createElement('div')
            refs.setAttribute('class', 'references')
            for refname, children in references:
                ref = xml.createElement('div')
                ref.setAttribute('class', 'reference')
                ref.setAttribute('id', 'ref:' + refname)
                refnum = xml.createElement('span')
                refnum.setAttribute('class', 'ref-label')
                refnum.appendChild(xml.createTextNode('[' + refname + ']'))
                ref.appendChild(refnum)
                ref.appendChild(xml.createTextNode(' '))
                for child in children:
                    ref.appendChild(child)
                refs.appendChild(ref)
            el.parentNode.replaceChild(refs, el)

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

