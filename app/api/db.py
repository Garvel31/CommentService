import os

from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'postgresql://comments_username:comments_db_password@comments_db/comments_db_dev'
engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
