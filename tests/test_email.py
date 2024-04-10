import pytest
from notification_py.services.email import send_email
from notification_py.custom_types import (
    Message,
    Creds,
    EmailCreds,
    MessageDetails,
)
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("SMTP_USERNAME") or ""
password = os.getenv("SMTP_PASSWORD") or ""
smtp_server = os.getenv("SMTP_SERVER") or ""
smtp_port = os.getenv("SMTP_PORT") or ""
target_email = os.getenv("TARGET_EMAIL") or ""


@pytest.mark.asyncio
async def test_send_email():
    message = Message(
        message_details=MessageDetails(
            title="Test Title",
            text="Test Text",
            severity=2,
            source="Test Source",
            filename="Test Filename",
            line_number=0,
            time=datetime.now(),
        ),
        creds=Creds(
            email=EmailCreds(
                email=email,
                password=password,
                smtp_server=smtp_server,
                smtp_port=int(smtp_port),
                target_email=target_email,
            ),
            discord=None,
            slack=None,
        ),
    )
    result = await send_email(message)
    assert result.error is None
    assert result.success is True
