from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

SeverityLiteral = Literal[0, 1, 2, 3, 4, 5]


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


class TeamsCreds(BaseModel):
    webhook_url: str


class Creds(BaseModel):
    discord: Optional[DiscordCreds] = None
    slack: Optional[SlackCreds] = None
    email: Optional[EmailCreds] = None
    teams: Optional[TeamsCreds] = None


class MessageDetails(BaseModel):
    title: str
    text: str
    severity: SeverityLiteral
    source: str
    filename: Optional[str] = None
    line_number: Optional[int] = None
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
    teams: Optional[BasicAPIResponse] = None
