import aiohttp
from custom_types import Message


async def send_message_to_discord(message: Message):
    try:
        if message.creds and message.creds.discord:
            message.message = (
                f"<@{message.creds.discord.team_id}> {message.message}"  # noqa
            )
            url = f"https://discord.com/api/channels/{message.creds.discord.channel_id}/messages"  # noqa
            headers = {"Authorization": f"Bot {message.creds.discord.token}"}
            data = {
                "embeds": [
                    {
                        "title": message.title,
                        "description": message.message,
                        "color": message.severity,
                        "fields": [
                            {"name": "Source", "value": message.source},
                            {"name": "File", "value": message.filename},
                            {"name": "Line", "value": str(message.line_number)},  # noqa
                            {
                                "name": "Time",
                                "value": message.time.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),  # noqa
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
