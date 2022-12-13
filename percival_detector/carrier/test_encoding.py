'''
Created on 4 Dec 2014

@author: up45
'''

import unittest

from . import encoding
import struct

class TestEncodeMessage(unittest.TestCase):

    def test_single(self):
        '''Testing the encode_message() function with very basic inputs.'''
        result = encoding.encode_message(0x0005, 0x01020304)
        self.assertIsInstance(result, bytes, "Must return a byte array rather than %s"%type(result))
        self.assertEqual(result, b'\x00\x05\x01\x02\x03\x04', str([result]))
        
    def test_multi(self):
        '''Testing the encode_multi_message() function with very basic input'''
        result = encoding.encode_multi_message(0x000A, [0x01020304, 0x05060708])
        self.assertIsInstance(result, list, "Must return a list of byte arrays rather than %s"%type(result))
        self.assertIsInstance(result[0], bytes, "Must return a byte array rather than %s"%type(result))
        self.assertEqual(result, [b'\x00\x0A\x01\x02\x03\x04', b'\x00\x0B\x05\x06\x07\x08'], str([result]))
        
    def test_invalid_data_word(self):
        '''Testing encoding a single message with a too wide data word. This should raise an exception'''
        with self.assertRaises(struct.error):
            encoding.encode_message(0xAABB, 0x01020304050607)
    
    def test_invalid_address(self):
        '''Testing encodign of a single message with a too wide address parameter. This should raise and exception'''
        with self.assertRaises(struct.error):
            encoding.encode_message(0xAABBCC, 0x01020304)

class TestDecodeMessage(unittest.TestCase):
    def test_basic(self):
        '''Basic sanity check of the decode_message() function'''
        result = encoding.decode_message(b'\x00\x05\x01\x02\x03\x04')
        self.assertIsInstance(result, list, "Must be a 2D list rather than %s"%type(result))
        self.assertGreater(len(result), 0, "Result list contain no items")
        addr, word = result[0]
        self.assertEqual(addr, 0x0005, "Address not decoded properly: %X"%addr)
        self.assertEqual(word, 0x01020304, "Word not decoded properly: %X"%word)

    def test_multi_response(self):
        '''Test decode_message() with a series of addr,word responses...'''
        result = encoding.decode_message(b'\xAA\xBB\x01\x02\x03\x04\xCC\xDD\x05\x06\x07\x08\xEE\xFF\x09\x10\x11\x12')
        self.assertIsInstance(result, list, "Must be a 2D list rather than %s"%type(result))
        self.assertEqual(len(result), 3, "Not the expected number of responses in result (%d)"%len(result))
        addr, word = result[0]
        self.assertEqual(addr, 0xAABB, "Address[%d] not decoded properly: %X"%(0, addr))
        self.assertEqual(word, 0x01020304, "Word[%d] not decoded properly: %X"%(0,word))
        addr, word = result[1]
        self.assertEqual(addr, 0xCCDD, "Address[%d] not decoded properly: %X"%(1, addr))
        self.assertEqual(word, 0x05060708,  "Word[%d] not decoded properly: %X"%(1,word))
        addr, word = result[2]
        self.assertEqual(addr, 0xEEFF, "Address[%d] not decoded properly: %X"%(2, addr))
        self.assertEqual(word, 0x09101112, "Word[%d] not decoded properly: %X"%(2,word))
        
    def test_response_extra_bytes(self):
        '''Test the decode_message() function when a message string is parsed with some additional rubbish bytes.
           It should throw away the additional bytes and return an otherwise sensible response'''
        result = encoding.decode_message(b'\x00\x05\x01\x02\x03\x04\xEE\xAA')
        self.assertIsInstance(result, list, "Must be a 2D list rather than %s"%type(result))
        self.assertGreater(len(result), 0, "Result list contain no items")
        addr, word = result[0]
        self.assertEqual(addr, 0x0005, "Address not decoded properly: %X"%addr)
        self.assertEqual(word, 0x01020304, "Word not decoded properly: %X"%word)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()