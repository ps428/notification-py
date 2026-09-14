import asyncio
from notification_py.custom_types import (
    Message,
    NotificationResponse,
    BasicAPIResponse,
)

from notification_py.services.slack import send_message_to_slack
from notification_py.services.discord import send_message_to_discord
from notification_py.services.email import send_email
from notification_py.services.teams import send_message_to_teams


async def send_notification(message: Message) -> NotificationResponse:
    try:
        tasks = []
        task_keys = []

        if message.creds.slack:
            slack_message = message.model_copy(deep=True)
            tasks.append(send_message_to_slack(slack_message))
            task_keys.append("slack")

        if message.creds.discord:
            discord_message = message.model_copy(deep=True)
            tasks.append(send_message_to_discord(discord_message))
            task_keys.append("discord")

        if message.creds.email:
            email_message = message.model_copy(deep=True)
            tasks.append(send_email(email_message))
            task_keys.append("email")

        if message.creds.teams:
            teams_message = message.model_copy(deep=True)
            tasks.append(send_message_to_teams(teams_message))
            task_keys.append("teams")

        if not tasks:
            return NotificationResponse(
                success=False,
                message="No message sent!",
                error="No creds provided!",
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        provider_results = {}

        for index, result in enumerate(results):
            key = task_keys[index]
            if isinstance(result, BasicAPIResponse):
                if not result.success:
                    raise ValueError(result.error)
                provider_results[key] = result
            elif isinstance(result, Exception):
                raise result

        return NotificationResponse(
            success=True,
            message="Message sent successfully!",
            error=None,
            slack=provider_results.get("slack"),
            discord=provider_results.get("discord"),
            email=provider_results.get("email"),
            teams=provider_results.get("teams"),
        )
    except Exception as e:
        return NotificationResponse(
            success=False,
            message="Error sending notification!",
            error=str(e),
        )
