import aiohttp
from notification_py.custom_types import (
    BasicAPIResponse,
    Message,
    SeverityLiteral,
)


async def send_message_to_slack(message: Message) -> BasicAPIResponse:
    try:
        if message.creds and message.creds.slack:

            if not message.creds.slack:
                return BasicAPIResponse(
                    success=False,
                    message=None,
                    error="Slack credentials not provided",
                )

            url = message.creds.slack.webhook_url
            headers = {"Content-type": "application/json"}
            data = {
                "attachments": [
                    {
                        "fallback": (
                            f"New Alert - Severity:"
                            f" {message.message_details.severity}"
                        ),
                        "color": _get_color_for_severity(
                            message.message_details.severity
                        ),
                        "pretext": (
                            f"New Alert - Severity:"
                            f" {message.message_details.severity}"
                        ),
                        "title": message.message_details.title,
                        "text": f"<!channel>,\n{message.message_details.text}",
                        "fields": [
                            {
                                "title": "Source",
                                "value": message.message_details.source,
                                "short": False,
                            },
                            {
                                "title": "Filename",
                                "value": message.message_details.filename,
                                "short": True,
                            },
                            {
                                "title": "Line number",
                                "value": str(
                                    message.message_details.line_number
                                ),  # noqa
                                "short": True,
                            },
                            {
                                "title": "Time",
                                "value": message.message_details.time.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "short": False,
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
                                f"Failed to send message to Slack."
                                f" Status: {response.status}"
                            ),
                        )
            return BasicAPIResponse(success=True, message=None, error=None)
        else:
            return BasicAPIResponse(
                success=False,
                message=None,
                error="Slack credentials not provided",
            )
    except Exception as e:
        return BasicAPIResponse(success=False, message=None, error=str(e))


def _get_color_for_severity(severity: SeverityLiteral) -> str:
    severity_colors = {
        0: "#00FF00",  # Green
        1: "#0000FF",  # Blue
        2: "#FFFF00",  # Yellow
        3: "#FF8C00",  # Orange
        4: "#FF0000",  # Red
        5: "#000000",  # Black
    }
    return severity_colors.get(
        severity, "#FFFFFF"
    )  # Default to black if severity is not recognized
