from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# For now we use SQLite (simple file database, no setup needed)
# In Phase 8 we upgrade to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./neuroregen.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This function gives us a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()