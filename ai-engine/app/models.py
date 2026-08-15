from pydantic import BaseModel
from typing import Optional


class PodStatus(BaseModel):
    name: str
    namespace: str
    status: str


class Incident(BaseModel):
    pod: str
    namespace: str
    status: str
    analysis: Optional[str] = None


class JiraResult(BaseModel):
    key: Optional[str] = None
    id: Optional[str] = None
    created: Optional[bool] = None
    duplicate: Optional[bool] = None
    updated: Optional[bool] = None


class NotificationResult(BaseModel):
    sent: bool
    channel: str
    jira_key: Optional[str] = None
    pod: str
    recipient: Optional[str] = None