import pytest
from src.services.slack import send_message_to_slack
from custom_types import Message, Creds, SlackCreds, MessageDetails
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url = os.getenv("SLACK_WEBHOOK_URL") or ""


@pytest.mark.asyncio
async def test_send_message_to_slack():
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
            slack=SlackCreds(webhook_url=webhook_url),
            discord=None,
            email=None,
        ),
    )
    result = await send_message_to_slack(message)
    assert result.error is None
    assert result.success is True
