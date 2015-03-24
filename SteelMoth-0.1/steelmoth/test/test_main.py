#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock
from steelmoth.main import *  # @UnusedWildImport


class BaseFixture(object):
    def setUp(self):
        self.udm = UserDataManager()
class BaseTests(BaseFixture, unittest.TestCase):
    def testInitValuesOk(self):
        self.assertEqual(self.udm.iid,
                         {'': {'widget': None,
                               'children': [],
                               'grid': {}}})
    def testInsertExistingIidRaisesKeyError(self):
        self.assertRaises(KeyError,
                          self.udm.insert, '', 'end', '', None)
    def testDeleteNonexistentIidRaisesKeyError(self):
        self.assertRaises(KeyError,
                          self.udm.delete, 'nonexistent')


class SingleIidFixture(BaseFixture):
    def setUp(self):
        super().setUp()
        self.test_iid = 'singleiid'
        self.udm.insert('', 'end', self.test_iid, None)
class SingleIidTests(SingleIidFixture, unittest.TestCase):
    def testInsertSingleIidOk(self):
        self.assertIn(self.test_iid, self.udm.iid)
        self.assertEqual(len(self.udm.iid), 2)
        self.assertEqual(self.udm.iid[self.test_iid],
                         {'widget': None,
                          'children': [],
                          'grid': {}})
        self.assertEqual(self.udm.iid[''],
                         {'widget': None,
                          'children': [self.test_iid],
                          'grid': {}})


class SingleMockFixture(BaseFixture):
    def setUp(self):
        super().setUp()
        self.w = MagicMock()
        self.w.destroy = MagicMock(name='destroy')
        self.test_iid = 'mockiid'
        self.udm.insert('', 'end', self.test_iid, self.w)
class SingleMockTests(SingleMockFixture, unittest.TestCase):
    def testDeleteSingleMockOk(self):
        self.udm.delete(self.test_iid)
        self.assertEqual(len(self.udm.iid), 1)
        self.assertNotIn(self.test_iid, self.udm.iid)
        self.w.destroy.assert_called_once_with()


class MultipleMocksFixture(SingleMockFixture):
    def setUp(self):
        super().setUp()
        self.w1 = MagicMock()
        self.w2 = MagicMock()
        self.w1.destroy = MagicMock(name='w1.destroy')
        self.w2.destroy = MagicMock(name='w2.destroy')
        self.test_iid1 = 'mockiid1'
        self.test_iid2 = 'mockiid2'
        self.udm.insert(self.test_iid, 'end', self.test_iid1, self.w1)
        self.udm.insert(self.test_iid, 'end', self.test_iid2, self.w2)
class MultipleMocksTests(MultipleMocksFixture, unittest.TestCase):
    def testDeleteMultipleMocksOk(self):
        self.udm.delete(self.test_iid)
        
        self.assertEqual(len(self.udm.iid), 1)
        self.assertNotIn(self.test_iid, self.udm.iid)
        self.assertNotIn(self.test_iid1, self.udm.iid)
        self.assertNotIn(self.test_iid2, self.udm.iid)
        
        self.w.destroy.assert_called_once_with()
        self.assertFalse(self.w1.destroy.called)
        self.assertFalse(self.w2.destroy.called)


if __name__ == '__main__': unittest.main()