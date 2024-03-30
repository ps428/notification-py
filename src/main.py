from custom_types import Message, BasicAPIResponse


async def send_notification(message: Message) -> BasicAPIResponse:
    try:
        target_services = message.target_services
        # Send the message to all services
        if target_services == "all":
            # Send the message to Discord
            # Send the message to Slack
            pass

        # Send the message to Discord
        elif target_services == "discord":
            pass

        # Send the message to Slack
        elif target_services == "slack":
            pass

        # Send the response
        return BasicAPIResponse(
            success=True, message="Message sent successfully!", error=None
        )
    except Exception as e:
        raise e
