from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api import db_models, db_crud, schemas
from api.db import engine, SessionLocal

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/comments/openapi.json", docs_url="/api/v1/comments/docs")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/threads/", response_model=List[schemas.CommentThread])
def read_threads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    threads = db_crud.get_threads(db, skip=skip, limit=limit)
    return threads


@app.post("/thread/", response_model=schemas.CommentThread)
def create_thread(db: Session = Depends(get_db)):
    return db_crud.create_threads(db=db)


@app.post("/comment/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return db_crud.create_comment(db=db, comment=comment)


@app.get("/comments/", response_model=List[schemas.Comment])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db_crud.get_comments(db, skip=skip, limit=limit)
    return comments


@app.get("/comment/{comment_sid}", response_model=schemas.Comment)
def read_comment(comment_sid: UUID, db: Session = Depends(get_db)):
    db_comment = db_crud.get_comment_by_sid(db, comment_sid=comment_sid)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.put("/comment/{comment_sid}", response_model=schemas.Comment)
async def update_item(comment_sid: UUID, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    db_comment = db_crud.update_comment(db, comment_sid, comment)
    return db_comment
