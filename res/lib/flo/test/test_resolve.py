import unittest

from ..resolve import *

class TestResolver(unittest.TestCase):
    def setUp(self):
        self.resolver = Resolver('.') # XXX base is dummy

    def tearDown(self):
        del self.resolver

    def test_select_candidate(self):
        select_candidate = self.resolver.select_candidate

        files = [('index.ko.html', 'index', 'text/html', None, 'ko'),
                 ('index.en.html', 'index', 'text/html', None, 'en'),
                 ('index.ja.txt', 'index', 'text/plain', None, 'ja'),
                 ('index.zh.txt.gz', 'index', 'text/plain', 'gzip', 'zh')]
        #self.assertEqual(select_candidate(files, [(1000, 'ko', 

