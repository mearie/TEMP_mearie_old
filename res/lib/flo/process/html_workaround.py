"""(X)HTML workarounds for legacy browsers.
"""

from __future__ import absolute_import, division, with_statement

from .xmltree import XMLTreeProcessor

class HTMLLangWorkaround(XMLTreeProcessor):
    def __call__(self, context, xml):
        assert xml is not None

        body = xml.getElementsByTagName('body')[0]
        lang = body.getAttribute('lang')
        if lang:
            cls = body.getAttribute('class')
            body.setAttribute('class', (cls + ' lang-%s'%lang) if cls else 'lang-%s'%lang)
            body.setAttributeNS('http://www.w3.org/XML/1998/namespace', 'xml:lang', lang)
            body.setAttribute('lang', lang)

        for el in body.getElementsByTagName('*'):
            lang = el.getAttribute('lang')
            if lang:
                cls = el.getAttribute('class')
                el.setAttribute('class', (cls + ' lang-%s'%lang) if cls else 'lang-%s'%lang)
                el.setAttributeNS('http://www.w3.org/XML/1998/namespace', 'xml:lang', lang)
                el.setAttribute('lang', lang)

        return xml

