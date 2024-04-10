import asyncio
from notification_py.custom_types import (
    Message,
    NotificationResponse,
    BasicAPIResponse,
)

from notification_py.services.slack import send_message_to_slack
from notification_py.services.discord import send_message_to_discord
from notification_py.services.email import send_email


async def send_notification(message: Message) -> NotificationResponse:
    try:
        tasks = []

        if message.creds.slack:
            slack_message = message.model_copy(deep=True)
            tasks.append(send_message_to_slack(slack_message))

        if message.creds.discord:
            discord_message = message.model_copy(deep=True)
            tasks.append(send_message_to_discord(discord_message))

        if message.creds.email:
            email_message = message.model_copy(deep=True)
            tasks.append(send_email(email_message))

        if not tasks:
            return NotificationResponse(
                success=False,
                message="No message sent!",
                error="No creds provided!",
                slack=None,
                discord=None,
                email=None,
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        result_slack = None
        result_discord = None
        result_email = None

        for index, result in enumerate(results):
            if isinstance(result, BasicAPIResponse):
                if not result.success:
                    raise ValueError(result.error)
                if index == 0 and message.creds.slack:
                    result_slack = result
                elif index == 1 and message.creds.discord:
                    result_discord = result
                elif index == 2 and message.creds.email:
                    result_email = result
            elif isinstance(result, Exception):
                raise result

        # Send the response
        return NotificationResponse(
            success=True,
            message="Message sent successfully!",
            error=None,
            slack=result_slack,
            discord=result_discord,
            email=result_email,
        )
    except Exception as e:
        return NotificationResponse(
            success=False,
            message="Error sending notification!",
            error=str(e),
            slack=None,
            discord=None,
            email=None,
        )
