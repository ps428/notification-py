from src.services.discord import send_message_to_discord
from custom_types import Message, Creds, DiscordCreds
import asyncio
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("DISCORD_BOT_TOKEN")
channel_id = os.getenv("DISCORD_CHANNEL_ID")
team_id = os.getenv("DISCORD_TEAM_ID")


message = Message(
    message_details={
        "title": "Test Title",
        "text": "Test Text",
        "severity": 2,
        "source": "Test Source",
        "filename": "Test Filename",
        "line_number": 0,
        "time": datetime.now(),
    },
    creds=Creds(
        discord=DiscordCreds(
            token=bot_token, channel_id=channel_id, team_id=team_id
        )  # noqa
    ),
)
asyncio.run(send_message_to_discord(message))
