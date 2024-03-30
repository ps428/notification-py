from custom_types import Message, Creds, EmailCreds

import asyncio
from datetime import datetime

from src.services.email import send_email

from dotenv import load_dotenv

import os

load_dotenv()

email = os.getenv("SMTP_USERNAME")
password = os.getenv("SMTP_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
target_email = os.getenv("TARGET_EMAIL")

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
        email=EmailCreds(
            email=email,
            password=password,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            target_email=target_email,
        )
    ),
)

asyncio.run(send_email(message))
