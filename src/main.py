from custom_types import Message, NotificationResponse

from src.services.slack import send_message_to_slack
from src.services.discord import send_message_to_discord
from src.services.email import send_email


async def send_notification(message: Message) -> NotificationResponse:
    try:
        result_slack = None
        result_discord = None
        result_email = None

        if message.creds.slack:

            result_slack = await send_message_to_slack(message)
            if not result_slack.success:
                raise ValueError(result_slack.error)

        if message.creds.discord:

            result_discord = await send_message_to_discord(message)
            if not result_discord.success:
                raise ValueError(result_discord.error)

        if message.creds.email:

            result_email = await send_email(message)
            if not result_email.success:
                raise ValueError(result_email.error)

        if not result_slack and not result_discord and not result_email:
            return NotificationResponse(
                success=False,
                message="No message sent!",
                error="No creds provided!",
                slack=None,
                discord=None,
                email=None,
            )

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
