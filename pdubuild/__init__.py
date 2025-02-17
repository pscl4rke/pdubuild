

import io

from .sms_submit import SmsSubmit


def build(
) -> str:
    output = io.StringIO()
    sms_submit = SmsSubmit()
    sms_submit.render_to(output)
    return output.getvalue()
