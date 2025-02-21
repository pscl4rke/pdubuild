

from typing import Iterator, List
import io

from .sms_submit import DataEncoding, UserData, SmsSubmit


def split(chunksize: int, source: str) -> List[str]:
    output = []
    i = 0
    while i < len(source):
        output.append(source[i:(i + chunksize)])
        i += chunksize
    return output


def build(
        smsc: str,
        dest: str,
        message: str,
) -> Iterator[str]:
    encoding = DataEncoding.UCS2
    chunks = split(encoding.maxchunksize, message)
    for i, chunk in enumerate(chunks):
        output = io.StringIO()
        userdata = UserData(total_parts=len(chunks), sequence_number=(i + 1),
                            encoding=encoding, message=chunk)
        sms_submit = SmsSubmit(smsc=smsc, dest=dest, userdata=userdata)
        sms_submit.render_to(output)
        yield output.getvalue()
