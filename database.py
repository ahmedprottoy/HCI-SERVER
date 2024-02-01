from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DB_URL
import threading

DATABASE_URL = DB_URL

db_engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, pool_size=10, max_overflow=20, pool_recycle=3600)
SessionLocal = sessionmaker(bind=db_engine)

# Create a thread-local session
session_factory = scoped_session(SessionLocal, scopefunc=threading.current_thread)

Base = declarative_base()

def get_db():
    db = None
    try:
        db = session_factory()
        yield db
    finally:
        db.close()