import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from custom_types import Message


async def send_email(message: Message):
    if message.creds is None or message.creds.email is None:
        raise ValueError("Email credentials are missing.")

    message = _update_message(message)
    email_creds = message.creds.email

    # Create a multipart message
    email_message = MIMEMultipart()
    email_message["From"] = email_creds.email
    email_message["To"] = email_creds.target_email
    email_message["Subject"] = message.message_details.title

    # Create the body of the email
    body = f"Severity: {message.message_details.severity}\n"
    body += f"Source: {message.message_details.source}\n"
    body += f"Filename: {message.message_details.filename}\n"
    body += f"Line Number: {message.message_details.line_number}\n"
    body += f"Time: {message.message_details.time}\n\n"
    body += message.message_details.text

    # Attach the body to the email message
    email_message.attach(MIMEText(body, "plain"))

    try:
        # Create a connection to the SMTP server
        server = aiosmtplib.SMTP(
            hostname=email_creds.smtp_server,
            port=email_creds.smtp_port,
            use_tls=False,  # noqa
        )
        await server.connect()
        await server.login(email_creds.email, email_creds.password)
        await server.send_message(email_message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")


def _update_message(message: Message) -> Message:
    message.message_details.title = (
        f"{message.message_details.title} - "
        f"{message.message_details.source} | "
        f"Severity: {message.message_details.severity}"
    )
    message.message_details.text = f"To: {message.creds.email.target_email}\n{message.message_details.text}"  # noqa
    return message