from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

ServicesLiteral = Literal["all", "discord", "slack", "email"]


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


class Message(BaseModel):
    title: str
    message: str
    source: str
    severity: int
    filename: str
    line_number: int
    time: datetime
    target_services: Optional[ServicesLiteral] = "all"
    creds: Optional[Creds] = None


class BasicAPIResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    message: Optional[str] = None
