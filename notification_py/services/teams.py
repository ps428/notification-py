import aiohttp
from notification_py.custom_types import (
    BasicAPIResponse,
    Message,
    SeverityLiteral,
)


async def send_message_to_teams(message: Message) -> BasicAPIResponse:
    try:
        if message.creds and message.creds.teams:

            if not message.creds.teams:
                return BasicAPIResponse(
                    success=False,
                    message=None,
                    error="Teams credentials not provided",
                )

            url = message.creds.teams.webhook_url
            headers = {"Content-type": "application/json"}

            body_elements = [
                {
                    "type": "TextBlock",
                    "text": message.message_details.title,
                    "size": "Large",
                    "weight": "Bolder",
                    "wrap": True,
                },
                {
                    "type": "TextBlock",
                    "text": (
                        f"Alert - Severity:"
                        f" {message.message_details.severity}"
                    ),
                    "color": _get_color_for_severity(
                        message.message_details.severity
                    ),
                    "weight": "Bolder",
                    "spacing": "None",
                },
                {
                    "type": "TextBlock",
                    "text": message.message_details.text,
                    "wrap": True,
                },
                {
                    "type": "FactSet",
                    "facts": _build_facts(message),
                },
            ]

            data = {
                "type": "message",
                "attachments": [
                    {
                        "contentType": (
                            "application/vnd.microsoft.card.adaptive"
                        ),
                        "contentUrl": None,
                        "content": {
                            "$schema": (
                                "http://adaptivecards.io/schemas/"
                                "adaptive-card.json"
                            ),
                            "type": "AdaptiveCard",
                            "version": "1.2",
                            "body": body_elements,
                        },
                    }
                ],
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, json=data, headers=headers
                ) as response:
                    response_body = await response.text()
                    if response.status != 200:
                        return BasicAPIResponse(
                            success=False,
                            message=None,
                            error=(
                                f"Failed to send message to Teams."
                                f" Status: {response.status}"
                            ),
                        )
                    # Teams returns 429 rate-limit errors
                    # in the response body, not as HTTP status
                    if "error" in response_body.lower() or (
                        "429" in response_body
                    ):
                        return BasicAPIResponse(
                            success=False,
                            message=None,
                            error=(
                                f"Teams webhook error: {response_body}"
                            ),
                        )
            return BasicAPIResponse(success=True, message=None, error=None)
        else:
            return BasicAPIResponse(
                success=False,
                message=None,
                error="Teams credentials not provided",
            )
    except Exception as e:
        return BasicAPIResponse(success=False, message=None, error=str(e))


def _build_facts(message: Message) -> list:
    facts = [
        {
            "title": "Source",
            "value": message.message_details.source,
        },
    ]
    if message.message_details.filename is not None:
        facts.append(
            {
                "title": "Filename",
                "value": message.message_details.filename,
            }
        )
    if message.message_details.line_number is not None:
        facts.append(
            {
                "title": "Line number",
                "value": str(message.message_details.line_number),
            }
        )
    facts.append(
        {
            "title": "Time",
            "value": message.message_details.time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
    )
    return facts


def _get_color_for_severity(severity: SeverityLiteral) -> str:
    severity_colors = {
        0: "Good",       # Green
        1: "Accent",     # Blue
        2: "Warning",    # Yellow
        3: "Warning",    # Orange
        4: "Attention",  # Red
        5: "Attention",  # Black/Critical
    }
    return severity_colors.get(severity, "Default")
