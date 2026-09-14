import pytest
from notification_py.services.teams import send_message_to_teams
from notification_py.custom_types import (
    Message,
    Creds,
    TeamsCreds,
    MessageDetails,
)
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url = os.getenv("TEAMS_WEBHOOK_URL") or ""


@pytest.mark.asyncio
async def test_send_message_to_teams():
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
            teams=TeamsCreds(webhook_url=webhook_url),
        ),
    )
    result = await send_message_to_teams(message)
    assert result.error is None
    assert result.success is True


@pytest.mark.asyncio
async def test_send_generic_message_to_teams():
    message = Message(
        message_details=MessageDetails(
            title="New Customer Onboarded",
            text="Acme Corp has been successfully onboarded.",
            severity=0,
            source="CRM System",
            time=datetime.now(),
        ),
        creds=Creds(
            teams=TeamsCreds(webhook_url=webhook_url),
        ),
    )
    result = await send_message_to_teams(message)
    assert result.error is None
    assert result.success is True
