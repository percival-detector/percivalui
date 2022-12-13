'''
Created on 8 May 2015

@author: up45
'''
import unittest

class TestImports(unittest.TestCase):

    def testImportPercivalCarrier(self):
        """import percival_detector.carrier"""
        import percival_detector.carrier
        
    def testImportPercivalDetector(self):
        """import percival_detector.control"""
        import percival_detector.control
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
