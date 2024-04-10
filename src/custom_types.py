from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

SeverityLiteral = Literal[0, 1, 2, 3, 4]


class EmailCreds(BaseModel):
    email: str
    password: str
    smtp_server: str
    smtp_port: int
    target_email: str


class DiscordCreds(BaseModel):
    token: str
    channel_id: int
    team_id: int


class SlackCreds(BaseModel):
    webhook_url: str


class Creds(BaseModel):
    discord: Optional[DiscordCreds]
    slack: Optional[SlackCreds]
    email: Optional[EmailCreds]


class MessageDetails(BaseModel):
    title: str
    text: str
    severity: SeverityLiteral
    source: str
    filename: str
    line_number: int
    time: datetime


class Message(BaseModel):
    message_details: MessageDetails
    creds: Creds


class BasicAPIResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    message: Optional[str] = None


class NotificationResponse(BasicAPIResponse):
    slack: Optional[BasicAPIResponse] = None
    discord: Optional[BasicAPIResponse] = None
    email: Optional[BasicAPIResponse] = None
