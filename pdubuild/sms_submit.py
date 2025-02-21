

from dataclasses import dataclass
from enum import Enum
from typing import TextIO

from .util import digits_flipped_for_octets, encode_ucs2


class DataEncoding(Enum):
    UCS2 = (8, 67)

    def __init__(self, identifier, maxchunksize):
        self.identifier = identifier
        self.maxchunksize = maxchunksize

    @classmethod
    def from_alias(self, alias: str) -> "DataEncoding":
        if alias in ("ucs2",):
            return DataEncoding.UCS2
        else:
            raise ValueError("Unknown encoding: %r" % alias)


@dataclass
class UserData:
    total_parts: int
    sequence_number: int
    encoding: DataEncoding
    message: str

    def has_header(self) -> bool:
        return True  # FIXME

    def render_header(self) -> str:
        header_body = "".join((
            self.render_concat_16bit_block(),
        ))
        header_body_len = len(header_body) // 2
        return ("%02X" % header_body_len) + header_body

    def render_concat_16bit_block(self) -> str:
        return "".join((
            "0804B49F",  # FIXME stuff
            "%02X" % self.total_parts,
            "%02X" % self.sequence_number,
        ))

    def render_body(self) -> str:
        if self.encoding is DataEncoding.UCS2:
            return encode_ucs2(self.message)
        else:
            raise NotImplementedError(repr(self.encoding))

    def rendered_octet_length(self) -> int:
        return (len(self.render_header()) + len(self.render_body())) // 2


@dataclass
class SmsSubmit:
    smsc: str
    dest: str
    userdata: UserData
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
        if self.userdata.has_header():
            status += 64
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
        stream.write("00")  # TP-PID (protocol identifier)
        stream.write("%02X" % self.userdata.encoding.identifier)
        stream.write("FF")  # Maximum validity
        # Write the message
        stream.write("%02X" % self.userdata.rendered_octet_length())
        stream.write(self.userdata.render_header())
        stream.write(self.userdata.render_body())
