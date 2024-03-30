import aiohttp
from custom_types import Message


async def send_message_to_discord(message: Message):
    try:
        if message.creds and message.creds.discord:
            message = _update_message(message)
            url = (
                f"https://discord.com/api/channels/"
                f"{message.creds.discord.channel_id}/messages"
            )
            headers = {"Authorization": f"Bot {message.creds.discord.token}"}
            data = {
                "embeds": [
                    {
                        "title": message.message_details.title,
                        "description": message.message_details.text,
                        "color": message.message_details.severity,
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
                                "value": message.message_details.time.strftime(
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
                        print(
                            f"Failed to send message to Discord. "
                            f"Status code: {response.status}"
                        )
        else:
            print("Discord credentials not provided.")
            raise Exception("Discord credentials not provided.")
    except Exception as e:
        raise e


def _update_message(message: Message) -> Message:
    message.message_details.title = (
        f"{message.message_details.title} - "
        f"{message.message_details.source} | "
        f"Severity: {message.message_details.severity}"
    )
    message.message_details.text = (
        f"<@{message.creds.discord.team_id}>,\n{message.message_details.text}"
    )
    message.message_details.severity = _update_severity_color(
        message.message_details.severity
    )
    return message


def _update_severity_color(severity: int) -> int:
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
