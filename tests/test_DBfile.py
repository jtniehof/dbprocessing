#!/usr/bin/env python
from __future__ import print_function

import datetime
import unittest
from distutils.dir_util import copy_tree, remove_tree
import os
import tempfile

from dbprocessing import DBfile
from dbprocessing import DButils
from dbprocessing import Diskfile
from dbprocessing import Version

class DBfileTests(unittest.TestCase):
    """Tests for DBfile class"""
    
    def setUp(self):
        super(DBfileTests, self).setUp()
        self.tempD = tempfile.mkdtemp()

        copy_tree('testDB/', self.tempD)

        self.dbu = DButils.DButils(self.tempD + '/testDB.sqlite')

        #Update the mission path to the tmp dir
        self.dbu.getEntry('Mission', 1).rootdir = self.tempD
        self.dbu.commitDB()
        self.dbu.MissionDirectory = self.dbu.getMissionDirectory()

    def tearDown(self):
        super(DBfileTests, self).tearDown()
        remove_tree(self.tempD)

    def createDummyDBF(self, fname):
        dbf = DBfile.DBfile(self.tempD + fname, self.dbu, makeDiskFile=True)
        dbf.diskfile.params['utc_file_date'] = datetime.date.today()
        dbf.diskfile.params['utc_start_time'] = datetime.date.today()
        dbf.diskfile.params['utc_stop_time'] = datetime.date.today() + datetime.timedelta(days=1)
        dbf.diskfile.params['data_level'] = 0
        dbf.diskfile.params['file_create_date'] = datetime.date.today()
        dbf.diskfile.params['exists_on_disk'] = 1
        dbf.diskfile.params['product_id'] = 1
        dbf.diskfile.params['shasum'] = Diskfile.calcDigest(self.tempD + fname)
        dbf.diskfile.params['version'] = Version.Version(1, 2, 3)
        dbf.diskfile.params['newest_version'] = 1

        return dbf

    def test_invalidInput(self):
        self.assertRaises(DBfile.DBfileError, DBfile.DBfile, self.tempD + '/L0/testDB_000_first.raw', self.dbu)

    def test_repr(self):
        dbf = DBfile.DBfile(self.tempD + '/L0/testDB_000_first.raw', self.dbu, makeDiskFile=True)
        self.assertTrue(dbf.__repr__().startswith("<DBfile.DBfile object: "))

    def test_getDirectory(self):
        dbf = DBfile.DBfile(self.tempD + '/L0/testDB_000_first.raw', self.dbu, makeDiskFile=True)
        
        self.assertRaises(DBfile.DBfileError, dbf.getDirectory )

        dbf.diskfile.params['product_id'] = 4
        self.assertEqual( self.tempD + '/L0', dbf.getDirectory() )

    def test_addFileToDB(self):
        with open(self.tempD + '/file.file', 'w') as fp:
            fp.write('I am some test data\n')
        dbf = self.createDummyDBF('/file.file')

        self.assertTrue(dbf.addFileToDB())

    def test_move1(self):
        with open(self.tempD + '/file.file', 'w') as fp:
            fp.write('I am some test data\n')
        dbf = self.createDummyDBF('/file.file')

        real_ans = (self.tempD + '/file.file', self.tempD + '/L1/file.file')
        self.assertEqual(real_ans, dbf.move())

    def test_move2(self):
        with open(self.tempD + '/file.file', 'w') as fp:
            fp.write('I am some test data\n')
        os.symlink(self.tempD + '/file.file', self.tempD + '/sym.file')
        dbf = self.createDummyDBF('/sym.file')

        real_ans = (self.tempD + '/sym.file', self.tempD + '/L1/sym.file')
        self.assertTrue(os.path.isfile(self.tempD + '/sym.file'))
        self.assertEqual(real_ans, dbf.move())
        self.assertFalse(os.path.isfile(self.tempD + '/sym.file'))

    def test_move3(self):
        with open(self.tempD + '/file.file', 'w') as fp:
            fp.write('I am some test data\n')
        dbf = self.createDummyDBF('/file.file')

        remove_tree(self.tempD+'/L1')

        real_ans = (self.tempD + '/file.file', self.tempD + '/L1/file.file')
        self.assertFalse(os.path.isdir(self.tempD + '/L1'))
        self.assertEqual(real_ans, dbf.move())
        self.assertTrue(os.path.isdir(self.tempD + '/L1'))

if __name__ == "__main__":
    unittest.main()
