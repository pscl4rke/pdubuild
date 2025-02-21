

import io

from .sms_submit import DataEncoding, UserData, SmsSubmit


def build(
        smsc: str,
        dest: str,
        message: str,
) -> str:
    output = io.StringIO()
    userdata = UserData(total_parts=1, sequence_number=1,
                        encoding=DataEncoding.UCS2, message=message)
    sms_submit = SmsSubmit(smsc=smsc, dest=dest, userdata=userdata)
    sms_submit.render_to(output)
    return output.getvalue()
