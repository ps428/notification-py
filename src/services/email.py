import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from custom_types import Message


def send_email(message: Message):
    if message.creds is None or message.creds.email is None:
        raise ValueError("Email credentials are missing.")

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
        # Create a secure SSL/TLS connection to the SMTP server
        with smtplib.SMTP(
            email_creds.smtp_server, email_creds.smtp_port
        ) as server:  # noqa
            server.starttls()
            server.login(email_creds.email, email_creds.password)
            server.send_message(email_message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
