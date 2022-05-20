"""action.py describes the action a robot takes."""

from typing import List, Optional

from pydantic import BaseModel
from pydantic.schema import datetime

from app.schemas.actions.action import Action


class ActionSequence(BaseModel):
    title: str = ""
    version: Optional[str] = None
    last_change: datetime = datetime.min
    actions: List[Action] = []

    def __init__(self, title: str, version: Optional[str], last_change: datetime, actions: List[Action]):
        super().__init__()
        self.title = title
        self.version = version
        self.last_change = last_change
        self.actions = actions
