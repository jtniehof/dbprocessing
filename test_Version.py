#!/usr/bin/env python2.6

import unittest

import Version


__version__ = '2.0.3'


class VersionTests(unittest.TestCase):
    """Tests of the Version class"""

    def test_interfaceOne(self):
        """Interface version starts at 1"""
        self.assertRaises(Version.VersionError, Version.Version, 0, 0, 0)

    def test_Version_inc(self):
        """The versions should increment"""
        ver = Version.Version(1, 0, 0)
        ver.incRevision()
        self.assertEqual(Version.Version(1, 0, 1), ver)
        ver.incQuality()
        self.assertEqual(Version.Version(1, 1, 1), ver)
        ver.incInterface()
        self.assertEqual(Version.Version(2, 1, 1), ver)

    def test_Version_repr(self):
        """__repr__ should have a known output"""
        invals = ( Version.Version(1, 0, 1), Version.Version(5, 0, 1),
                  Version.Version(1, 3, 1) )
        answers = ( '1.0.1', '5.0.1', '1.3.1' )
        for i, val in enumerate(invals):
            self.assertEqual(answers[i], str(val))

    def test_Version_eq(self):
        """__eq__ should work"""
        invals = (  (Version.Version(1, 0, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 2, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 0, 4), Version.Version(1, 0, 0)),
                        (Version.Version(4, 2, 1), Version.Version(1, 0, 0)) )
        real_ans = (True, False, False, False)
        for i, val in enumerate(invals):
            self.assertEqual(real_ans[i], val[0] == val[1])

    def test_Version_ne(self):
        """__ne__ should work"""
        invals = (  (Version.Version(1, 0, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 2, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 0, 4), Version.Version(1, 0, 0)),
                        (Version.Version(4, 2, 1), Version.Version(1, 0, 0)) )
        real_ans = (False, True, True, True)
        for i, val in enumerate(invals):
            self.assertEqual(real_ans[i], val[0] != val[1])

    def test_Version_gt(self):
        """__gt__ should work"""
        invals = (  (Version.Version(1, 0, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 2, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 0, 4), Version.Version(1, 0, 0)),
                        (Version.Version(4, 2, 1), Version.Version(1, 0, 99)) )
        real_ans = (False, True, True, True)
        for i, val in enumerate(invals):
            self.assertEqual(real_ans[i], val[0] > val[1])

    def test_Version_lt(self):
        """__lt__ should work"""
        invals = (  (Version.Version(1, 0, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 2, 0), Version.Version(1, 0, 0)),
                        (Version.Version(1, 0, 4), Version.Version(1, 0, 0)),
                        (Version.Version(4, 2, 1), Version.Version(5, 0, 0)),
                        (Version.Version(5, 2, 1), Version.Version(5, 3, 0)),
                        (Version.Version(5, 0, 1), Version.Version(5, 0, 4)) )
        real_ans = (False, False, False, True, True, True)
        for i, val in enumerate(invals):
            self.assertEqual(real_ans[i], val[0] < val[1])

    def test_checkVersion(self):
        """_checkVersion should raise VersionError"""
        self.assertRaises(ValueError, Version.Version, 'string', 0, 0)
        self.assertRaises(ValueError, Version.Version, 0, 'string', 0)
        self.assertRaises(ValueError, Version.Version, 0, 0, 'string')




if __name__ == "__main__":
    unittest.main()