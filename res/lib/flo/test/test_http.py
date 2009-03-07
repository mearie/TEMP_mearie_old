import unittest

from ..http import *

class TestAccept(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(
                tokenize('text/html; charset=utf-8; q=1.0, text/*; q=0.5, */*'),
                ['text', '/', 'html', ';', 'charset', '=', 'utf-8', ';', 'q', '=',
                 '1.0', ',', 'text', '/', '*', ';', 'q', '=', '0.5', ',', '*', '/', '*'])
        self.assertEqual(tokenize('"foo\\"bar"'), ['"foo\\"bar"'])

    def test_parse(self):
        self.assertEqual(
                parse_accept('text/html; q=1.0, text/*; q=0.5, */*'),
                [(1000, ('text', 'html'), []), (1000, (None, None), []),
                 (500, ('text', None), [])])

