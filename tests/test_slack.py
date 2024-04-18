import pytest
from notification_py.services.slack import send_message_to_slack
from notification_py.custom_types import (
    Message,
    Creds,
    SlackCreds,
    MessageDetails,
)
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url = os.getenv("SLACK_WEBHOOK_URL") or ""


@pytest.mark.asyncio
async def test_send_message_to_slack():
    message = Message(
        message_details=MessageDetails(
            title="No Food!",
            text="Pizza is out of stock. This is critical!",
            severity=4,
            source="Pizza Store",
            filename="pizza.py",
            line_number=23,
            time=datetime.now(),
        ),
        creds=Creds(
            slack=SlackCreds(webhook_url=webhook_url),
            discord=None,
            email=None,
        ),
    )
    result = await send_message_to_slack(message)
    assert result.error is None
    assert result.success is True
