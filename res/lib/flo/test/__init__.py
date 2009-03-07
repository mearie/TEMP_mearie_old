import os
import imp
import unittest

class TestProgram(unittest.TestProgram):
    def __init__(self, *args, **kwargs):
        unittest.TestProgram.__init__(self, defaultTest='dummy', *args, **kwargs)

    def findTests(self, dir=None):
        if dir is None:
            dir = os.path.dirname(__file__)

        tests = []
        for f in os.listdir(dir):
            if f.startswith('test_') and f.endswith(os.extsep + 'py'):
                mod = imp.load_source('flo.test.' + f[:-3], os.path.join(dir, f))
                tests.append(mod)
        return tests

    def createTests(self):
        self.test = unittest.TestSuite()
        loader = unittest.defaultTestLoader
        for mod in self.findTests():
            self.test.addTest(loader.loadTestsFromModule(mod))

main = TestProgram

if __name__ == '__main__':
    main()

