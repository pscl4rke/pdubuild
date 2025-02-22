

import unittest

from pdubuild import build


class TestExample(unittest.TestCase):

    def test_single_ucs2(self):
        pdus = list(build(
            smsc="+447785016005",
            dest="07493574689",
            message="f0 Hi John it's me",
            encodewith="ucs2",
        ))
        self.assertEqual(pdus, [
            # One PDU:
            "079144775810065051000B817094534786F90008FF2B0"
            "60804B49F0101006600300020004800690020004A006F"
            "0068006E002000690074002700730020006D0065"
        ])

    def test_single_gsm7(self):
        pdus = list(build(
            smsc="+447785016005",
            dest="07493574689",
            message="Hello there seven bit version local dest  ",
            encodewith="gsm7",
        ))
        self.assertEqual(pdus, [
            # One PDU:
            "079144775810065011000B817094534786F90000FF2AC"
            "8329BFD06D1D1657919342FDBCB6E90384D07D9CBF279"
            "FAED06B1DFE3301B442ECFE92010"
        ])
