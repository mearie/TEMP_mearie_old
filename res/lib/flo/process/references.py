"""Extracts references and footnotes, and places them to given container.

`ref` or `fn` pseudo-element is used for references and footnotes (which are
treated as same), and the processor places them to next `references` or
`footnotes` pseudo-element. `ref`/`fn` can be nested, and `references`/
`footnotes` can contain other `ref`/`fn` (placed in that position) so one can
use `name` attribute to point the latter description. e.g.

    <p>something<ref>foo</ref><ref>bar<ref>quux</ref></ref>
        here<ref name="blah"/></p>
    <references>
        <ref name="blah">and blah is placed here</ref>
    </references>

is rendered to something like following:

    <p>something<a href="#ref:1">[1]</a><a href="#ref:2">[2]</a>
        here<a href="#ref:4">[4]</a></p>
    <div class="footnotes">
        <p id="ref:1">[1] foo</p>
        <p id="ref:2">[2] bar<a href="#ref:3">[3]</a></p>
        <p id="ref:3">[3] quux</p>
        <p id="ref:4">[4] and blah is placed here</p>
    </div>
"""

from __future__ import absolute_import, division, with_statement

from .xmltree import XMLTREETYPE

class ReferenceProcessor(object):
    """Processes ref/fn and references/footnotes pseudo-element to actual
    (X)HTML. The former introduces a link to actual footnote, and the latter
    prints all previous footnotes into container.
    
    Input format should be XML tree."""

    input_type = [XMLTREETYPE]
    output_type = XMLTREETYPE

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

