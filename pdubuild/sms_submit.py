

from typing import TextIO


class SmsSubmit:

    def render_to(self, stream: TextIO) -> None:
        # Write the SMSC
        stream.write("0791447758100650")  # FIXME
        # Write the bitmask
        stream.write("51")  # FIXME
        # Write the message reference
        stream.write("00")  # FIXME
        # Write the destination
        stream.write("0B817094534786F9")  # FIXME
        # Write assorted metadata
        stream.write("0008FF")  # FIXME
        # Write the message
        stream.write("2B")  # len  # FIXME
        stream.write("060804B49F0101006600300020004800690020004A006F0068006E002000690074002700730020006D0065")  # FIXME
