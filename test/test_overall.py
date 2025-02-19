

import unittest

from pdubuild import build


EXAMPLE = "079144775810065051000B817094534786F90008FF2B0" \
          "60804B49F0101006600300020004800690020004A006F" \
          "0068006E002000690074002700730020006D0065"


class TestExample(unittest.TestCase):

    def test_example(self):
        pdu = build(
            smsc="+447785016005",
            dest="07493574689",
            message="f0 Hi John it's me",
        )
        self.assertEqual(pdu, EXAMPLE)
