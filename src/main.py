from custom_types import Message, BasicAPIResponse
from print_position import print_pos_time as print


async def send_notification(message: Message) -> BasicAPIResponse:
    try:
        # TODO
        print("Sending notification...")
        target_services = message.target_services
        # Send the message to all services
        if target_services == "all":
            # Send the message to Discord
            # Send the message to Slack
            # Send the message to Email
            pass

        # Send the message to Discord
        elif target_services == "discord":
            pass

        # Send the message to Slack
        elif target_services == "slack":
            pass

        # Send the message to Email
        elif target_services == "email":
            pass

        # Send the response
        return BasicAPIResponse(
            success=True, message="Message sent successfully!", error=None
        )
    except Exception as e:
        raise e
