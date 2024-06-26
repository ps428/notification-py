import pytest
from notification_py.main import send_notification
from notification_py.custom_types import (
    DiscordCreds,
    Message,
    Creds,
    EmailCreds,
    MessageDetails,
    SlackCreds,
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


bot_token = os.getenv("DISCORD_BOT_TOKEN") or ""
channel_id = os.getenv("DISCORD_CHANNEL_ID") or 0
team_id = os.getenv("DISCORD_TEAM_ID") or 0


webhook_url = os.getenv("SLACK_WEBHOOK_URL") or ""


@pytest.mark.asyncio
async def test_notification():

    message = Message(
        message_details=MessageDetails(
            # title="All good",
            # text="Sufficient amount of pizzas in stock.",
            # severity=0,
            # title="Low food",
            # text="Only 10 pizzas left.",
            # severity=2,
            title="No Food!",
            text="Pizza is out of stock. This is critical!",
            severity=4,
            source="Pizza Store",
            filename="pizza.py",
            line_number=23,
            time=datetime.now(),
        ),
        creds=Creds(
            discord=DiscordCreds(
                token=bot_token,
                channel_id=int(channel_id),
                team_id=int(team_id),
            ),
            slack=SlackCreds(webhook_url=webhook_url),
            email=EmailCreds(
                email=email,
                password=password,
                smtp_server=smtp_server,
                smtp_port=int(smtp_port),
                target_email=target_email,
            ),
        ),
    )
    result = await send_notification(message)
    assert result.error is None
    assert result.success is True

    assert result.discord is not None
    assert result.discord.error is None
    assert result.discord.success is True

    assert result.slack is not None
    assert result.slack.error is None
    assert result.slack.success is True

    assert result.email is not None
    assert result.email.error is None
    assert result.email.success is True


@pytest.mark.asyncio
async def test_notification_failure():

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
            discord=None,
            slack=None,
            email=None,
        ),
    )
    result = await send_notification(message)
    assert result.error == "No creds provided!"
    assert result.success is False

    assert result.discord is None

    assert result.slack is None
    assert result.email is None
