# coding=utf-8

LANGUAGES = ['en', 'ko', 'ja']

from mearie.markdown import markdown
md = markdown

def indent(s):
    if not s.strip(): return ''
    return '\n\t' + s.strip('\r\n').replace('\n', '\n\t')

def uri_to_path(c, uri):
    if '://' in uri: return None
    try:
        lookup = c.lookup
    except:
        c = c.context
        lookup = c.lookup
    return lookup.convert_to_path(lookup.adjust_uri(uri, c['topmost'].uri)) 

def canonical(c, preservelang=True):
    uri = '/' + c['topmost'].uri.lstrip('/')
    if uri.endswith('.txt'): uri = uri[:-4]
    if not preservelang and uri[-3:-2] == ':' and uri[-2:] in LANGUAGES: uri = uri[:-3]
    return uri

class Language(object):
    def __init__(self, lang):
        self.lang = lang
        assert lang in LANGUAGES

    def __call__(self, default=None, **strings):
        try:
            return strings[self.lang]
        except KeyError:
            for lang in LANGUAGES:
                if lang in strings: return strings[lang]
            else:
                if default is not None: return default
                raise

    def __str__(self):
        return self.lang

    def __repr__(self):
        return 'Language(%r)' % self.lang

