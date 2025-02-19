

from dataclasses import dataclass
from typing import TextIO

from .util import digits_flipped_for_octets


@dataclass
class SmsSubmit:
    smsc: str

    def render_to(self, stream: TextIO) -> None:
        # Write the SMSC
        smsc_repr = digits_flipped_for_octets(self.smsc.lstrip("+"))
        stream.write("%02x" % ((len(smsc_repr) // 2) + 1))
        if self.smsc.startswith("+"):
            stream.write("91")
        else:
            stream.write("81")
        stream.write(smsc_repr)
        # Write the bitmask
        stream.write("51")  # FIXME
        # Write the message reference
        stream.write("00")  # FIXME
        # Write the destination
        stream.write("0B")  # FIXME
        stream.write("81")  # FIXME
        stream.write(digits_flipped_for_octets("07493574689"))  # FIXME
        # Write assorted metadata
        stream.write("0008FF")  # FIXME
        # Write the message
        stream.write("2B")  # len  # FIXME
        stream.write("060804B49F0101006600300020004800690020004A006F0068006E002000690074002700730020006D0065")  # FIXME
