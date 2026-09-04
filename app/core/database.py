import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv() # Loads variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Creating SQLAlchemy connection
# FastAPI -> SQLAlchemy -> psycog -> PostgresSQL
engine = create_engine(DATABASE_URL)

# Open and close session
# Basically a unit of interaction with the database
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()