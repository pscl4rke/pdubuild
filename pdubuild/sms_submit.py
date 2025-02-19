

from dataclasses import dataclass
from typing import TextIO

from .util import digits_flipped_for_octets, encode_ucs2


@dataclass
class SmsSubmit:
    smsc: str
    dest: str
    message_reference: int = 0
    reject_duplicates: bool = False
    status_report_request: bool = False
    reply_path: bool = False

    def status_octet(self) -> int:
        status = 1  # bits 0 and 1 indicate SMS-SUBMIT
        if self.reject_duplicates:
            status += 4
        status += 16  # assume relative validity FIXME
        if self.status_report_request:
            status += 32
        status += 64  # FIXME don't always have user-data header
        if self.reply_path:
            status += 128
        return status

    def render_to(self, stream: TextIO) -> None:
        # Write the SMSC
        smsc_repr = digits_flipped_for_octets(self.smsc.lstrip("+"))
        stream.write("%02X" % ((len(smsc_repr) // 2) + 1))
        if self.smsc.startswith("+"):
            stream.write("91")
        else:
            stream.write("81")
        stream.write(smsc_repr)
        # Write the bitmask
        stream.write("%02X" % self.status_octet())
        # Write the message reference
        stream.write("%02X" % self.message_reference)
        # Write the destination
        stream.write("%02X" % len(self.dest.lstrip("+")))
        if self.dest.startswith("+"):
            stream.write("91")
        else:
            stream.write("81")
        stream.write(digits_flipped_for_octets(self.dest.lstrip("+")))
        # Write assorted metadata
        stream.write("0008FF")  # FIXME
        # Write the message
        stream.write("2B")  # len  # FIXME
        stream.write("060804B49F0101")  # FIXME
        stream.write(encode_ucs2("f0 Hi John it's me"))
