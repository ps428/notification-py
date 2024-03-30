from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

ServicesLiteral = Literal["all", "discord", "slack", "email"]
SeverityLiteral = Literal[0, 1, 2, 3, 4]


class EMail(BaseModel):
    email: str
    password: str
    smtp_server: str
    smtp_port: int
    imap_server: str
    imap_port: int
    imap_folder: str
    target_email: str


class DiscordCreds(BaseModel):
    token: str
    channel_id: int
    team_id: int


class SlackCreds(BaseModel):
    token: str
    channel_id: str


class Creds(BaseModel):
    discord: Optional[DiscordCreds] = None
    slack: Optional[SlackCreds] = None
    email: Optional[EMail] = None


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
    targeted_services: Optional[ServicesLiteral] = "all"
    creds: Optional[Creds] = None


class BasicAPIResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    message: Optional[str] = None
