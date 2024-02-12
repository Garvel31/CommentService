from __future__ import annotations
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import List, Optional, Union

from .db_models import CommentThreads


class CommentBase(BaseModel):
    user_id: UUID
    body: str
    thread_id: UUID
    historical_body: Union[str, None] = None
    histori_body: Union[str, None] = None


class CommentUpdate(BaseModel):
    body: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    """Для вывода данных."""
    sid: UUID
    thread: CommentThreadBase
    creation_date: datetime
    modification_date: datetime

    class Config:
        orm_mode = True


class CommentThreadBase(BaseModel):
    sid: UUID
    creation_date: datetime
    modification_date: datetime


class CommentThreadsCreate(CommentThreadBase):
    pass


class CommentThread(CommentThreadBase):

    comments: List[Comment] = []

    class Config:
        orm_mode = True
