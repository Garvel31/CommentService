import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base


class Comments(Base):
    __tablename__ = 'comments'

    sid = Column('sid', UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    user_id = Column('user', UUID(as_uuid=True))
    body = Column('body', String(250))
    thread_id = Column(UUID(as_uuid=True), ForeignKey('comment_threads.sid'))
    historical_body = Column('historical_body', String(250), nullable=True)
    histori_body = Column('histori_body', String(250), nullable=True)
    creation_date = Column('creation_date', DateTime, default=datetime.utcnow)
    modification_date = Column('modification_date', DateTime, default=datetime.utcnow)

    thread = relationship('CommentThreads', back_populates='comments')


class CommentThreads(Base):
    __tablename__ = 'comment_threads'

    sid = Column('sid', UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    creation_date = Column('creation_date', DateTime, default=datetime.utcnow)
    modification_date = Column('modification_date', DateTime, default=datetime.utcnow)

    comments = relationship('Comments', back_populates='thread')
