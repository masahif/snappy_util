#!/usr/bin/env python

import os, sys
sys.path.append(os.pardir)
from snappy_util import snappy_java
import unittest

class TestFunctions(unittest.TestCase):
    def test1(self):
        f = snappy_java.open('data1.txt.snappy')
        self.assertEqual(type(f), snappy_java.SnappyJavaFile)
        self.assertEqual(f.readline(), "abcdefg\n")
        self.assertEqual(f.readline(), "ABCDEFG\n")
        self.assertEqual(f.readline(), "hijklmn\n")
        self.assertEqual(f.readline(), "HIJKLMN\n")
        self.assertEqual(f.readline(), "")
        f.close()


    def test2(self):
        f = snappy_java.SnappyJavaFile('data1.txt.snappy')
        self.assertEqual(f.readline(), "abcdefg\n")
        self.assertEqual(f.readline(), "ABCDEFG\n")
        self.assertEqual(f.readline(), "hijklmn\n")
        self.assertEqual(f.readline(), "HIJKLMN\n")
        self.assertEqual(f.readline(), "")
        f.close()
        

if __name__ == '__main__':
    unittest.main()


