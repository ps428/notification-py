import aiohttp
from custom_types import (
    DiscordCreds,
    Message,
    BasicAPIResponse,
    SeverityLiteral,
)


async def send_message_to_discord(message: Message) -> BasicAPIResponse:
    try:
        if message.creds.discord is not None:
            if isinstance(message.creds.discord, DiscordCreds):
                message = _update_message(message)

                if not message.creds.discord:
                    return BasicAPIResponse(
                        success=False,
                        message=None,
                        error="Discord credentials not provided",
                    )
                url = (
                    f"https://discord.com/api/channels/"
                    f"{message.creds.discord.channel_id}/messages"
                )
                headers = {
                    "Authorization": f"Bot {message.creds.discord.token}"
                }
                data = {
                    "embeds": [
                        {
                            "title": message.message_details.title,
                            "description": message.message_details.text,
                            "color": _get_color_for_severity(
                                message.message_details.severity
                            ),
                            "fields": [
                                {
                                    "name": "Error Source",
                                    "value": message.message_details.source,
                                },
                                {
                                    "name": "Filename",
                                    "value": message.message_details.filename,
                                },
                                {
                                    "name": "Line number",
                                    "value": str(
                                        message.message_details.line_number
                                    ),  # noqa
                                },
                                {
                                    "name": "Time",
                                    "value": message.message_details.time.strftime(  # noqa
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                },
                            ],
                        }
                    ]
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, json=data, headers=headers
                    ) as response:  # noqa
                        if response.status != 200:
                            return BasicAPIResponse(
                                success=False,
                                message=None,
                                error=(
                                    f"Failed to send message to Discord "
                                    f"Status: {response.status}"
                                ),
                            )
                return BasicAPIResponse(
                    success=True,
                    message="Message sent successfully!",
                    error=None,
                )

        else:
            return BasicAPIResponse(
                success=False,
                message=None,
                error="Discord credentials not provided",
            )
    except Exception as e:
        return BasicAPIResponse(
            success=False,
            message=None,
            error=f"Failed to send message to Discord: {e}",
        )
    return BasicAPIResponse(
        success=False,
        message=None,
        error="Failed to send message to Discord",
    )


def _update_message(message: Message) -> Message:
    message.message_details.title = (
        f"{message.message_details.title} - "
        f"{message.message_details.source} | "
        f"Severity: {message.message_details.severity}"
    )
    if not message.creds.discord:
        raise ValueError("Discord credentials not provided.")
    message.message_details.text = (
        f"<@&{message.creds.discord.team_id}>,\n{message.message_details.text}"
    )

    return message


def _get_color_for_severity(severity: SeverityLiteral) -> int:
    if severity == 0:
        return 5763719
    elif severity == 1:
        return 5793266
    elif severity == 2:
        return 16705372
    elif severity == 3:
        return 15418782
    elif severity == 4:
        return 15548997
    else:
        return 0x000000
