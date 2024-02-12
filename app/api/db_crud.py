from uuid import UUID

from sqlalchemy import update
from sqlalchemy.orm import Session
from starlette import schemas

from . import schemas, db_models


def get_comment_by_sid(db: Session, comment_sid: UUID):
    return db.query(db_models.Comments).filter(db_models.Comments.sid == comment_sid).first()


def get_comments_by_user(db: Session, user_id: UUID):
    return db.query(db_models.Comments).filter(db_models.Comments.user_id == user_id)


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Comments).offset(skip).limit(limit).all()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = db_models.Comments(
        user_id=comment.user_id,
        body=comment.body,
        thread_id=comment.thread_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_sid, comment: schemas.CommentUpdate):
    old_body = db.query(db_models.Comments).filter(db_models.Comments.sid == comment_sid).value()
    stmt = (
        update(
            db_models.Comments
        ).where(
            db_models.Comments.sid == comment_sid
        ).values(
            body=comment.body,
            historical_body=old_body
        )
    )

    db_comment = db_models.Comments(
        user_id=comment.user_id,
        body=comment.body,
        thread_id=comment.thread_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_threads(db: Session):
    db_thread = db_models.CommentThreads()
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread


def get_threads_by_sid(db: Session, comment_sid: UUID):
    return db.query(db_models.CommentThreads).filter(db_models.CommentThreads.sid == comment_sid).first()


def get_threads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.CommentThreads).offset(skip).limit(limit).all()
