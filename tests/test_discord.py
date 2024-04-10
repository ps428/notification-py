import pytest
from src.services.discord import send_message_to_discord
from src.custom_types import Message, Creds, DiscordCreds, MessageDetails
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("DISCORD_BOT_TOKEN") or ""
channel_id = os.getenv("DISCORD_CHANNEL_ID") or 0
team_id = os.getenv("DISCORD_TEAM_ID") or 0


@pytest.mark.asyncio
async def test_send_message_to_discord():
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
            discord=DiscordCreds(
                token=bot_token,
                channel_id=int(channel_id),
                team_id=int(team_id),
            ),
            slack=None,
            email=None,
        ),
    )
    result = await send_message_to_discord(message)
    assert result.error is None
    assert result.success is True
