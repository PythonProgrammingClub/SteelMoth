#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from steelmoth.main import *  # @UnusedWildImport


class Observable_Base_Fixture(object):
    def setUp(self):
        self.o = Observable()


class Observable_Base_Tests(Observable_Base_Fixture, unittest.TestCase):
    def testInitOk(self):
        self.assertEqual(self.o.observers, [])


class Observable_Observer_Fixture(Observable_Base_Fixture):
    def setUp(self):
        super().setUp()
        self.m = MagicMock()
        self.m.update = MagicMock(name='update')
        self.o.attach(self.m)


class Observable_Observer_Tests(Observable_Observer_Fixture,
                                unittest.TestCase):
    def testNotifyCallsUpdate(self):
        self.o.notify()
        self.m.update.assert_called_once_with()

    def testDetachNotifyDoesntCallUpdate(self):
        self.o.detach(self.m)
        self.o.notify()
        self.assertFalse(self.m.update.called)


class UserData_Base_Fixture(object):
    def setUp(self):
        self.udm = UserData()


class UserData_Base_Tests(UserData_Base_Fixture, unittest.TestCase):
    def testInitValuesOk(self):
        self.assertEqual(self.udm.iid, {'': {'widget': None,
                                             'configure': {},
                                             'children': [],
                                             'grid': {}}})

    def testInsertExistingIidRaisesKeyError(self):
        self.assertRaises(KeyError, self.udm.insert, '', 'end', '', None)

    def testDeleteNonexistentIidRaisesKeyError(self):
        self.assertRaises(KeyError, self.udm.delete, 'nonexistent')


class UserData_OneIid_Fixture(UserData_Base_Fixture):
    def setUp(self):
        super().setUp()
        self.test_iid = 'singleiid'
        self.udm.insert('', 'end', self.test_iid, None)


class UserData_OneIid_Tests(UserData_OneIid_Fixture, unittest.TestCase):
    def testInsertOneIidOk(self):
        self.assertIn(self.test_iid, self.udm.iid)
        self.assertEqual(len(self.udm.iid), 2)
        self.assertEqual(self.udm.iid[self.test_iid], {'widget': None,
                                                       'configure': {},
                                                       'children': [],
                                                       'grid': {}})
        self.assertEqual(self.udm.iid[''], {'widget': None,
                                            'configure': {},
                                            'children': [self.test_iid],
                                            'grid': {}})


class UserData_OneWidget_Fixture(UserData_Base_Fixture):
    def setUp(self):
        super().setUp()
        self.w = MagicMock()
        self.w.destroy = MagicMock(name='destroy')
        self.test_iid = 'mockiid'
        self.udm.insert('', 'end', self.test_iid, self.w)


class UserData_OneWidget_Tests(UserData_OneWidget_Fixture, unittest.TestCase):
    def testDeleteOneWidgetOk(self):
        self.udm.delete(self.test_iid)
        self.assertEqual(len(self.udm.iid), 1)
        self.assertNotIn(self.test_iid, self.udm.iid)
        self.w.destroy.assert_called_once_with()


class UserData_TwoChildWidgets_Fixture(UserData_OneWidget_Fixture):
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


class UserData_TwoChildWidgets_Tests(UserData_TwoChildWidgets_Fixture,
                                     unittest.TestCase):
    def testDeleteParentWidgetCascadesDelete(self):
        self.udm.delete(self.test_iid)
        self.assertEqual(len(self.udm.iid), 1)
        self.assertNotIn(self.test_iid, self.udm.iid)
        self.assertNotIn(self.test_iid1, self.udm.iid)
        self.assertNotIn(self.test_iid2, self.udm.iid)
        self.w.destroy.assert_called_once_with()
        self.assertFalse(self.w1.destroy.called)
        self.assertFalse(self.w2.destroy.called)


class Dialog_Base_Tests(unittest.TestCase):
    @patch("tkinter.Toplevel.wait_window")
    @patch("tkinter.Toplevel.focus_set")
    @patch("tkinter.Toplevel.geometry")
    @patch("tkinter.Toplevel.protocol")
    @patch("tkinter.Toplevel.grab_set")
    @patch("steelmoth.main.Dialog.buttonbox")
    @patch("tkinter.Frame.pack")
    @patch("tkinter.Frame.__init__", autospec=True, return_value=None)
    @patch("tkinter.Toplevel.transient")
    @patch("tkinter.Toplevel.__init__", autospec=True, return_value=None)
    def testInitOk(self,
                   tkinter_Toplevel___init__,  # @UnusedVariable
                   tkinter_Toplevel_transient,  # @UnusedVariable
                   tkinter_Frame___init__,  # @UnusedVariable
                   tkinter_Frame_pack,  # @UnusedVariable
                   steelmoth_main_Dialog_buttonbox,  # @UnusedVariable
                   tkinter_Toplevel_grab_set,  # @UnusedVariable
                   tkinter_Toplevel_protocol,  # @UnusedVariable
                   tkinter_Toplevel_geometry,  # @UnusedVariable
                   tkinter_Toplevel_focus_set,  # @UnusedVariable
                   tkinter_Toplevel_wait_window):  # @UnusedVariable
        p = MagicMock()
        d = Dialog(p)  # @UnusedVariable


if __name__ == '__main__':
    unittest.main()
