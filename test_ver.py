import unittest

import pytest

from pytest_ver import pth
# import socket_oneline


# -------------------
class TestOneline(unittest.TestCase):

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        pass

    # --------------------
    @classmethod
    def tearDownClass(cls):
        pth.term()

    # --------------------
    def test_0(self):
        # # declare a new protcol id and it's description
        # pth.proto.protocol('tp-000', 'basic pass/fail tests')
        # pth.proto.set_dut_serialno('sn-0123')
        #
        # pth.proto.step('try checks with 1 failure')
        # pth.ver.verify_equal(1, 2, reqids='SRS-001')
        # pth.ver.verify_equal(1, 1, reqids='SRS-002')
        # pth.ver.verify_equal(1, 1, reqids='SRS-003')
        # pth.proto.comment('should be 1 failure and 2 passes')
        pass

