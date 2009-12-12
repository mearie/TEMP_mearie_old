# coding=utf-8

from mearie.markdown import markdown
md = markdown

LANGUAGES = ['en', 'ko', 'ja']

class Language(object):
    def __init__(self, lang):
        self.lang = lang
        assert lang in LANGUAGES

    def __call__(self, **strings):
        try:
            return strings[self.lang]
        except KeyError:
            for lang in LANGUAGES:
                if lang in strings: return strings[lang]
            else: raise

    def __str__(self):
        return self.lang

    def __repr__(self):
        return 'Language(%r)' % self.lang

