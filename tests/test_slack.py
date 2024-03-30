from datetime import datetime
from custom_types import Message, Creds, SlackCreds
from src.services.slack import send_message_to_slack
import asyncio

from dotenv import load_dotenv

import os

load_dotenv()

webhook_url = os.getenv("SLACK_WEBHOOK_URL")

message = Message(
    message_details={
        "title": "Test Title",
        "text": "Test Text",
        "severity": 3,
        "source": "Test Source",
        "filename": "Test Filename",
        "line_number": 0,
        "time": datetime.now(),
    },
    creds=Creds(slack=SlackCreds(webhook_url=webhook_url)),
)

asyncio.run(send_message_to_slack(message))
