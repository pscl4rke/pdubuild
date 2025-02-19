

import io

from .sms_submit import SmsSubmit


def build(
    smsc: str,
) -> str:
    output = io.StringIO()
    sms_submit = SmsSubmit(smsc=smsc)
    sms_submit.render_to(output)
    return output.getvalue()
